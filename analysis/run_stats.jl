using Distributed
using ProgressMeter
@everywhere using JupyterParameters

analysis_folder = @__DIR__
cd(analysis_folder)

@everywhere const proteins = readlines(abspath("..", "benchmark_list.txt"))

@showprogress pmap(proteins) do protein
    try
        notebook_file = joinpath(pwd(), protein,
            "03_Stats.ipynb")
        jjnbparam([
            "03_Stats.ipynb",
            notebook_file,
            "--timeout", "-1",
            "--protein", protein])
        # --execute --ExecutePreprocessor.timeout=-1
        run(`jupyter-nbconvert.exe --to html $notebook_file`)
    catch err
        logfile_path = joinpath("logfiles", "stats_errors.log")
        open(logfile_path, "a") do logfile
            println(logfile, "$protein ERROR: $err")
        end
    end
end
