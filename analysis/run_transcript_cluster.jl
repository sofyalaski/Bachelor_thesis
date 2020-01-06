using Distributed
using ProgressMeter
@everywhere using JupyterParameters

analysis_folder = @__DIR__
cd(analysis_folder)

@everywhere const proteins = readlines(abspath("..", "benchmark_list.txt"))

@showprogress pmap(proteins) do protein
    try
        notebook_file = joinpath(pwd(), protein,
            "02_Transcript_clustering.ipynb")
        jjnbparam([
            "02_Transcript_clustering.ipynb",
            notebook_file,
            "--timeout", "-1",
            "--protein", protein])
        run(`jupyter-nbconvert.exe --to html $notebook_file`)
    catch err
        logfile_path = joinpath("logfiles", "transcript_cluster_errors.log")
        open(logfile_path, "a") do logfile
            println(logfile, "$protein ERROR: $err")
        end
    end
end
