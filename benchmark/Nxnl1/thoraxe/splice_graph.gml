
        graph [
            directed 1
            id 42
            label "splice graph of s-exons"
        
                node [
                    id 1
                    label "start"
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000016773,ENSDARG00000052035,ENSG00000171773,ENSGGOG00000002347,ENSMODG00000004441,ENSMUSG00000034829,ENSRNOG00000042658,ENSSSCG00000040328,ENSXETG00000020568"
                    transcripts "ENSBTAT00000022306,ENSDART00000143829,ENSGGOT00000002359,ENSMODT00000005590,ENSMUST00000163659,ENSRNOT00000024434,ENSRNOT00000080706,ENSSSCT00000065552,ENST00000301944,ENSXETT00000044438"
            
                ]
            
                node [
                    id 2
                    label "2_0"
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000016773,ENSDARG00000052035,ENSG00000171773,ENSGGOG00000002347,ENSMODG00000004441,ENSMUSG00000034829,ENSRNOG00000042658,ENSSSCG00000040328,ENSXETG00000020568"
                    transcripts "ENSBTAT00000022306,ENSDART00000143829,ENSGGOT00000002359,ENSMODT00000005590,ENSMUST00000163659,ENSRNOT00000024434,ENSRNOT00000080706,ENSSSCT00000065552,ENST00000301944,ENSXETT00000044438"
            
                        phylosofs "%"
                
                ]
            
                node [
                    id 3
                    label "1_0"
                    conservation 100.0
                    transcript_fraction 90.0
                    genes "ENSBTAG00000016773,ENSDARG00000052035,ENSG00000171773,ENSGGOG00000002347,ENSMODG00000004441,ENSMUSG00000034829,ENSRNOG00000042658,ENSSSCG00000040328,ENSXETG00000020568"
                    transcripts "ENSBTAT00000022306,ENSDART00000143829,ENSGGOT00000002359,ENSMODT00000005590,ENSMUST00000163659,ENSRNOT00000024434,ENSSSCT00000065552,ENST00000301944,ENSXETT00000044438"
            
                        phylosofs "("
                
                ]
            
                node [
                    id 4
                    label "stop"
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000016773,ENSDARG00000052035,ENSG00000171773,ENSGGOG00000002347,ENSMODG00000004441,ENSMUSG00000034829,ENSRNOG00000042658,ENSSSCG00000040328,ENSXETG00000020568"
                    transcripts "ENSBTAT00000022306,ENSDART00000143829,ENSGGOT00000002359,ENSMODT00000005590,ENSMUST00000163659,ENSRNOT00000024434,ENSRNOT00000080706,ENSSSCT00000065552,ENST00000301944,ENSXETT00000044438"
            
                ]
            
                node [
                    id 5
                    label "3_0"
                    conservation 11.11111111111111
                    transcript_fraction 10.0
                    genes "ENSGGOG00000002347"
                    transcripts "ENSGGOT00000002359"
            
                        phylosofs ")"
                
                ]
            
                node [
                    id 6
                    label "4_0"
                    conservation 11.11111111111111
                    transcript_fraction 10.0
                    genes "ENSMODG00000004441"
                    transcripts "ENSMODT00000005590"
            
                        phylosofs "+"
                
                ]
            
                node [
                    id 7
                    label "0_1"
                    conservation 11.11111111111111
                    transcript_fraction 10.0
                    genes "ENSRNOG00000042658"
                    transcripts "ENSRNOT00000080706"
            
                        phylosofs "0"
                
                ]
            
                edge [
                    source 1
                    target 2
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000016773,ENSDARG00000052035,ENSG00000171773,ENSGGOG00000002347,ENSMODG00000004441,ENSMUSG00000034829,ENSRNOG00000042658,ENSSSCG00000040328,ENSXETG00000020568"
                    transcripts "ENSBTAT00000022306,ENSDART00000143829,ENSGGOT00000002359,ENSMODT00000005590,ENSMUST00000163659,ENSRNOT00000024434,ENSRNOT00000080706,ENSSSCT00000065552,ENST00000301944,ENSXETT00000044438"
                ]
            
                edge [
                    source 2
                    target 3
                    conservation 100.0
                    transcript_fraction 90.0
                    genes "ENSBTAG00000016773,ENSDARG00000052035,ENSG00000171773,ENSGGOG00000002347,ENSMODG00000004441,ENSMUSG00000034829,ENSRNOG00000042658,ENSSSCG00000040328,ENSXETG00000020568"
                    transcripts "ENSBTAT00000022306,ENSDART00000143829,ENSGGOT00000002359,ENSMODT00000005590,ENSMUST00000163659,ENSRNOT00000024434,ENSSSCT00000065552,ENST00000301944,ENSXETT00000044438"
                ]
            
                edge [
                    source 3
                    target 4
                    conservation 77.77777777777779
                    transcript_fraction 70.0
                    genes "ENSBTAG00000016773,ENSDARG00000052035,ENSG00000171773,ENSMUSG00000034829,ENSRNOG00000042658,ENSSSCG00000040328,ENSXETG00000020568"
                    transcripts "ENSBTAT00000022306,ENSDART00000143829,ENSMUST00000163659,ENSRNOT00000024434,ENSSSCT00000065552,ENST00000301944,ENSXETT00000044438"
                ]
            
                edge [
                    source 3
                    target 5
                    conservation 11.11111111111111
                    transcript_fraction 10.0
                    genes "ENSGGOG00000002347"
                    transcripts "ENSGGOT00000002359"
                ]
            
                edge [
                    source 5
                    target 4
                    conservation 11.11111111111111
                    transcript_fraction 10.0
                    genes "ENSGGOG00000002347"
                    transcripts "ENSGGOT00000002359"
                ]
            
                edge [
                    source 3
                    target 6
                    conservation 11.11111111111111
                    transcript_fraction 10.0
                    genes "ENSMODG00000004441"
                    transcripts "ENSMODT00000005590"
                ]
            
                edge [
                    source 6
                    target 4
                    conservation 11.11111111111111
                    transcript_fraction 10.0
                    genes "ENSMODG00000004441"
                    transcripts "ENSMODT00000005590"
                ]
            
                edge [
                    source 2
                    target 7
                    conservation 11.11111111111111
                    transcript_fraction 10.0
                    genes "ENSRNOG00000042658"
                    transcripts "ENSRNOT00000080706"
                ]
            
                edge [
                    source 7
                    target 4
                    conservation 11.11111111111111
                    transcript_fraction 10.0
                    genes "ENSRNOG00000042658"
                    transcripts "ENSRNOT00000080706"
                ]
            
        ]
        