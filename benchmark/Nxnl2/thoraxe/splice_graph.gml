
        graph [
            directed 1
            id 42
            label "splice graph of s-exons"
        
                node [
                    id 1
                    label "start"
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000019958,ENSDARG00000003934,ENSG00000130045,ENSGGOG00000027419,ENSMMUG00000008414,ENSMODG00000013386,ENSMUSG00000021396,ENSRNOG00000014538,ENSSSCG00000035269,ENSXETG00000010869"
                    transcripts "ENSBTAT00000031535,ENSDART00000016103,ENSGGOT00000025486,ENSGGOT00000053860,ENSMMUT00000008032,ENSMODT00000017046,ENSMUST00000021828,ENSRNOT00000019489,ENSSSCT00000050066,ENST00000375855,ENSXETT00000023771"
            
                ]
            
                node [
                    id 2
                    label "1_0"
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000019958,ENSDARG00000003934,ENSG00000130045,ENSGGOG00000027419,ENSMMUG00000008414,ENSMODG00000013386,ENSMUSG00000021396,ENSRNOG00000014538,ENSSSCG00000035269,ENSXETG00000010869"
                    transcripts "ENSBTAT00000031535,ENSDART00000016103,ENSGGOT00000025486,ENSGGOT00000053860,ENSMMUT00000008032,ENSMODT00000017046,ENSMUST00000021828,ENSRNOT00000019489,ENSSSCT00000050066,ENST00000375855,ENSXETT00000023771"
            
                        phylosofs "%"
                
                ]
            
                node [
                    id 3
                    label "3_0"
                    conservation 80.0
                    transcript_fraction 72.72727272727273
                    genes "ENSBTAG00000019958,ENSDARG00000003934,ENSGGOG00000027419,ENSMODG00000013386,ENSMUSG00000021396,ENSRNOG00000014538,ENSSSCG00000035269,ENSXETG00000010869"
                    transcripts "ENSBTAT00000031535,ENSDART00000016103,ENSGGOT00000025486,ENSMODT00000017046,ENSMUST00000021828,ENSRNOT00000019489,ENSSSCT00000050066,ENSXETT00000023771"
            
                        phylosofs "("
                
                ]
            
                node [
                    id 4
                    label "stop"
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000019958,ENSDARG00000003934,ENSG00000130045,ENSGGOG00000027419,ENSMMUG00000008414,ENSMODG00000013386,ENSMUSG00000021396,ENSRNOG00000014538,ENSSSCG00000035269,ENSXETG00000010869"
                    transcripts "ENSBTAT00000031535,ENSDART00000016103,ENSGGOT00000025486,ENSGGOT00000053860,ENSMMUT00000008032,ENSMODT00000017046,ENSMUST00000021828,ENSRNOT00000019489,ENSSSCT00000050066,ENST00000375855,ENSXETT00000023771"
            
                ]
            
                node [
                    id 5
                    label "4_0"
                    conservation 20.0
                    transcript_fraction 18.181818181818183
                    genes "ENSG00000130045,ENSGGOG00000027419"
                    transcripts "ENSGGOT00000053860,ENST00000375855"
            
                        phylosofs ")"
                
                ]
            
                node [
                    id 6
                    label "2_0"
                    conservation 10.0
                    transcript_fraction 9.090909090909092
                    genes "ENSMMUG00000008414"
                    transcripts "ENSMMUT00000008032"
            
                        phylosofs "+"
                
                ]
            
                edge [
                    source 1
                    target 2
                    conservation 100.0
                    transcript_fraction 100.0
                    genes "ENSBTAG00000019958,ENSDARG00000003934,ENSG00000130045,ENSGGOG00000027419,ENSMMUG00000008414,ENSMODG00000013386,ENSMUSG00000021396,ENSRNOG00000014538,ENSSSCG00000035269,ENSXETG00000010869"
                    transcripts "ENSBTAT00000031535,ENSDART00000016103,ENSGGOT00000025486,ENSGGOT00000053860,ENSMMUT00000008032,ENSMODT00000017046,ENSMUST00000021828,ENSRNOT00000019489,ENSSSCT00000050066,ENST00000375855,ENSXETT00000023771"
                ]
            
                edge [
                    source 2
                    target 3
                    conservation 80.0
                    transcript_fraction 72.72727272727273
                    genes "ENSBTAG00000019958,ENSDARG00000003934,ENSGGOG00000027419,ENSMODG00000013386,ENSMUSG00000021396,ENSRNOG00000014538,ENSSSCG00000035269,ENSXETG00000010869"
                    transcripts "ENSBTAT00000031535,ENSDART00000016103,ENSGGOT00000025486,ENSMODT00000017046,ENSMUST00000021828,ENSRNOT00000019489,ENSSSCT00000050066,ENSXETT00000023771"
                ]
            
                edge [
                    source 3
                    target 4
                    conservation 80.0
                    transcript_fraction 72.72727272727273
                    genes "ENSBTAG00000019958,ENSDARG00000003934,ENSGGOG00000027419,ENSMODG00000013386,ENSMUSG00000021396,ENSRNOG00000014538,ENSSSCG00000035269,ENSXETG00000010869"
                    transcripts "ENSBTAT00000031535,ENSDART00000016103,ENSGGOT00000025486,ENSMODT00000017046,ENSMUST00000021828,ENSRNOT00000019489,ENSSSCT00000050066,ENSXETT00000023771"
                ]
            
                edge [
                    source 2
                    target 5
                    conservation 20.0
                    transcript_fraction 18.181818181818183
                    genes "ENSG00000130045,ENSGGOG00000027419"
                    transcripts "ENSGGOT00000053860,ENST00000375855"
                ]
            
                edge [
                    source 5
                    target 4
                    conservation 20.0
                    transcript_fraction 18.181818181818183
                    genes "ENSG00000130045,ENSGGOG00000027419"
                    transcripts "ENSGGOT00000053860,ENST00000375855"
                ]
            
                edge [
                    source 2
                    target 6
                    conservation 10.0
                    transcript_fraction 9.090909090909092
                    genes "ENSMMUG00000008414"
                    transcripts "ENSMMUT00000008032"
                ]
            
                edge [
                    source 6
                    target 4
                    conservation 10.0
                    transcript_fraction 9.090909090909092
                    genes "ENSMMUG00000008414"
                    transcripts "ENSMMUT00000008032"
                ]
            
        ]
        