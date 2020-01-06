using ProgressMeter

const benchmark_folder = @__DIR__
cd(benchmark_folder)

const proteins = readlines(abspath("..", "benchmark_list.txt"))

@showprogress map(proteins) do protein
    try
        run(pipeline(
        `transcript_query $protein --verbose -l species_list.txt`,
        stdout = joinpath("logfiles", "$(protein)_transcript_query_out.txt"),
        stderr = joinpath("logfiles", "$(protein)_transcript_query_err.txt")))
    catch err
        open(joinpath("logfiles", "download_data_errors.log"), "a") do logfile
            println(logfile, "$protein ERROR: $err")
        end
    end
end

# run(`julia.bat -p 12 throw_thoraxe.jl`)
