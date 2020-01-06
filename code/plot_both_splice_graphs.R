library(RCy3)

proteins <-
  read.delim("/home/sofya/Documents/TranscriptAnnotation/benchmark_list.txt",
             header = FALSE)
proteins <- as.character(proteins$V1)
proteins <- c(proteins[1:28],proteins[30:51])#NoGRIN1

style_file <- "/home/sofya/Documents/TranscriptAnnotation/analysis/styles_both.xml"

for (protein in proteins) {
  network_file <-
    paste(
      "/home/sofya/Documents/TranscriptAnnotation/analysis/",
      protein,
      "/rnaseq/both_splice_graphs.gml",
      sep = ""
    )
  if (file.exists(network_file)) {
    pdf_file <-
      paste(
        "/home/sofya/Documents/TranscriptAnnotation/analysis/",
        protein,
        "/plots/both_splice_graphs.pdf",
        sep = ""
      )
    session_file <-
      paste(
        "/home/sofya/Documents/TranscriptAnnotation/analysis/",
        protein,
        "/rnaseq/both_CytoscapeSession.cys",
        sep = ""
      )
    
    cat(paste(network_file, "\n"))
    
    importNetworkFromFile(network_file)
    
    cat("    ...imported!\n")
    
    sty <- importVisualStyles(style_file)
    setVisualStyle(sty)
    
    cat("    ...style applied!\n")
    
    layoutNetwork("hierarchical")
    
    cat("    ...layout applied!\n")
    
    exportImage(pdf_file, type = "PDF")
    
    cat("    ...pdf saved!\n")
    
    saveSession(session_file)
    
    cat("    ...session saved!\n")
    
    deleteAllNetworks()
  }
}

