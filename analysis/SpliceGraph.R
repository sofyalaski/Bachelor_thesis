library(RCy3)

proteins <- read.delim("C:\\Users\\Diego\\MASSIV\\TranscriptAnnotation\\benchmark_list.txt", header=FALSE)
proteins$V1 <- as.character(proteins$V1)
proteins <- proteins$V1 # [proteins$V1 != "KIF1A"] # problem

style_file <- "C:\\Users\\Diego\\MASSIV\\TranscriptAnnotation\\benchmark\\styles.xml"

for(protein in proteins){
  network_file <- paste("C:\\Users\\Diego\\MASSIV\\TranscriptAnnotation\\benchmark\\", 
                        protein, "\\thoraxe\\splice_graph.gml",  
                        sep="")
  pdf_file <- paste("C:\\Users\\Diego\\MASSIV\\TranscriptAnnotation\\analysis\\", 
                    protein, "\\splice_graph.pdf",  
                    sep="")
  session_file <- paste("C:\\Users\\Diego\\MASSIV\\TranscriptAnnotation\\analysis\\", 
                    protein, "\\CytoscapeSession.cys",  
                    sep="")
  
  if (file.exists(pdf_file)){
    file.remove(pdf_file)
  }
  if (file.exists(session_file)){
    file.remove(session_file)
  }
  
  cat(paste(network_file, "\n"))
  
  importNetworkFromFile(network_file)
  
  cat("    ...imported!\n")
  
  sty <- importVisualStyles(style_file)
  setVisualStyle(sty)
  
  cat("    ...style applied!\n")
  
  layoutNetwork("hierarchical")
  
  cat("    ...layout applied!\n")
  
  exportImage(pdf_file, type="PDF")
  
  cat("    ...pdf saved!\n")
  
  saveSession(session_file)
  
  cat("    ...session saved!\n")
  
  deleteAllNetworks()
}
