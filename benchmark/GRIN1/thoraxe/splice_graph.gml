
        graph [
            directed 1
            id 42
            label "splice graph of s-exons"
        
                node [
                    id 1
                    label "start"
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000044035,ENSG00000169258,ENSGGOG00000024915,ENSMMUG00000013284,ENSMODG00000005102,ENSMUSG00000069227,ENSSSCG00000014054"
                    transcripts "ENSBTAT00000061410,ENSGGOT00000030071,ENSMMUT00000018649,ENSMODT00000006412,ENSMUST00000099506,ENSSSCT00000015353,ENST00000303991"
            
                ]
            
                node [
                    id 2
                    label "1_0"
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000044035,ENSG00000169258,ENSGGOG00000024915,ENSMMUG00000013284,ENSMODG00000005102,ENSMUSG00000069227,ENSSSCG00000014054"
                    transcripts "ENSBTAT00000061410,ENSGGOT00000030071,ENSMMUT00000018649,ENSMODT00000006412,ENSMUST00000099506,ENSSSCT00000015353,ENST00000303991"
            
                        phylosofs "%"
                
                ]
            
                node [
                    id 3
                    label "stop"
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000044035,ENSG00000169258,ENSGGOG00000024915,ENSMMUG00000013284,ENSMODG00000005102,ENSMUSG00000069227,ENSSSCG00000014054"
                    transcripts "ENSBTAT00000061410,ENSGGOT00000030071,ENSMMUT00000018649,ENSMODT00000006412,ENSMUST00000099506,ENSSSCT00000015353,ENST00000303991"
            
                ]
            
                node [
                    id 4
                    label "2_0"
                    conservation 14.285714285714285
                    transcript_fraction 14.285714285714285
                    genes "ENSMODG00000005102"
                    transcripts "ENSMODT00000006412"
            
                        phylosofs "("
                
                ]
            
                edge [
                    source 1
                    target 2
                    conservation 85.71428571428571
                    transcript_fraction 85.71428571428571
                    genes "ENSBTAG00000044035,ENSG00000169258,ENSGGOG00000024915,ENSMMUG00000013284,ENSMUSG00000069227,ENSSSCG00000014054"
                    transcripts "ENSBTAT00000061410,ENSGGOT00000030071,ENSMMUT00000018649,ENSMUST00000099506,ENSSSCT00000015353,ENST00000303991"
                ]
            
                edge [
                    source 2
                    target 3
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000044035,ENSG00000169258,ENSGGOG00000024915,ENSMMUG00000013284,ENSMODG00000005102,ENSMUSG00000069227,ENSSSCG00000014054"
                    transcripts "ENSBTAT00000061410,ENSGGOT00000030071,ENSMMUT00000018649,ENSMODT00000006412,ENSMUST00000099506,ENSSSCT00000015353,ENST00000303991"
                ]
            
                edge [
                    source 1
                    target 4
                    conservation 14.285714285714285
                    transcript_fraction 14.285714285714285
                    genes "ENSMODG00000005102"
                    transcripts "ENSMODT00000006412"
                ]
            
                edge [
                    source 4
                    target 2
                    conservation 14.285714285714285
                    transcript_fraction 14.285714285714285
                    genes "ENSMODG00000005102"
                    transcripts "ENSMODT00000006412"
                ]
            
        ]
        