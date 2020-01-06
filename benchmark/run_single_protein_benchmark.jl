using ArgParse
using Retry

const benchmark_folder = @__DIR__
cd(benchmark_folder)

function parse_commandline()
    settings = ArgParseSettings()

    @add_arg_table settings begin
        "protein"
            help = "Protein name"
            required = true
        "--keep"
            help = "Do not delete the protein folder before running"
            action = :store_true
        "--aligner"
            help = "Multiple sequence aliner to be used by thoraxe"
            arg_type = String
            default = "wsl clustalo"
    end

    return parse_args(settings)
end

function main()
    args = parse_commandline()
    protein = args["protein"]
    aligner = args["aligner"]

    if isdir(protein) && !args["keep"]
        rm(protein, force=true, recursive=true)
    end

    if !isdir("logfiles")
        mkdir("logfiles")
    end

    stdout_query = joinpath("logfiles", "$(protein)_transcript_query_out.txt")
    stderr_query = joinpath("logfiles", "$(protein)_transcript_query_err.txt")

    @repeat 3 try
        if isfile(stdout_query)
            rm(stdout_query)
        end
        if isfile(stderr_query)
            rm(stderr_query)
        end
        run(
            pipeline(
                `transcript_query $protein --verbose -l species_list.txt`,
                stdout = stdout_query,
                stderr = stderr_query
                )
            )
    catch err
        @delay_retry if true end
    end

    stdout_thoraxe = joinpath("logfiles", "$(protein)_thoraxe_out.txt")
    stderr_thoraxe = joinpath("logfiles", "$(protein)_thoraxe_err.txt")

    if isfile(stdout_thoraxe)
        rm(stdout_thoraxe)
    end
    if isfile(stderr_thoraxe)
        rm(stderr_thoraxe)
    end

    run(
        pipeline(
            `thoraxe -i $protein -y --plot_chimerics -a $aligner -l species_list.txt`,
            stdout = stdout_thoraxe,
            stderr = stderr_thoraxe
            )
        )

    0
end

main()
