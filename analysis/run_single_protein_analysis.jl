using ArgParse
using JupyterParameters

const analysis_folder = @__DIR__
cd(analysis_folder)

function parse_commandline()
    settings = ArgParseSettings()

    @add_arg_table settings begin
        "protein"
            help = "Protein name"
            required = true
        "--keep"
            help = "Do not delete the protein folder before running"
            action = :store_true
    end

    return parse_args(settings)
end

function main()
    args = parse_commandline()
    protein = args["protein"]

    if isdir(protein) && !args["keep"]
        rm(protein, force=true, recursive=true)
    end

    msa_folder = abspath("..", "benchmark", protein, "thoraxe", "msa")
    for msa in readdir(msa_folder)
        msa_path = joinpath(msa_folder, msa)
        logo_file = replace(msa, ".fasta" => "_logo.eps")
        logo_folder = abspath(".", protein, "seqlogos")
        if !isdir(logo_folder)
            mkpath(logo_folder)
        end
        logo_path = joinpath(logo_folder, logo_file)
        run(`weblogo.exe -f $msa_path -o $logo_path -F eps`)
    end

    notebook_clustering = joinpath(analysis_folder,
                                   protein,
                                   "02_Transcript_clustering.ipynb")
    jjnbparam([
        "02_Transcript_clustering.ipynb",
        notebook_clustering,
        "--timeout", "-1",
        "--protein", protein])
    run(`jupyter-nbconvert.exe --to html $notebook_clustering`)

    notebook_stats = joinpath(analysis_folder, protein, "03_Stats.ipynb")
    jjnbparam([
        "03_Stats.ipynb",
        notebook_stats,
        "--timeout", "-1",
        "--protein", protein])
    run(`jupyter-nbconvert.exe --to html $notebook_stats`)

    0
end

main()
