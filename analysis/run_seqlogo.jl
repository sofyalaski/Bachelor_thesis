using Distributed
using ProgressMeter

analysis_folder = @__DIR__
cd(analysis_folder)

@everywhere const proteins = readlines(abspath("..", "benchmark_list.txt"))

@showprogress pmap(proteins) do protein
    try
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
    catch err
        logfile_path = joinpath("logfiles", "seqlogo_errors.log")
        open(logfile_path, "a") do logfile
            println(logfile, "$protein ERROR: $err")
        end
    end
end
