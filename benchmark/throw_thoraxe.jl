using Distributed
using ProgressMeter

benchmark_folder = @__DIR__
cd(benchmark_folder)

@everywhere const proteins = readlines(abspath("..", "benchmark_list.txt"))

@showprogress pmap(proteins) do protein
    try
        run(pipeline(
        `thoraxe -i $protein -y --plot_chimerics -a 'wsl clustalo' -l species_list.txt`,
        stdout = joinpath("logfiles", "$(protein)_thoraxe_out.txt"),
        stderr = joinpath("logfiles", "$(protein)_thoraxe_err.txt")))
    catch err
        open(joinpath("logfiles", "throw_thoraxe_errors.log"), "a") do logfile
            println(logfile, "$protein ERROR: $err")
        end
    end
end
