
	graph [
		directed 1
		id 42
		label "splice graph of orthologous exon groups"

			node [
				id 1
				label "start"
				state 50
				conservation "10 0 "
			]

			node [
				id 2
				label "1_0"
				state 50
				conservation "10 0 "
			]

			node [
				id 3
				label "stop"
				state 50
				conservation "10 0 "
			]

			node [
				id 4
				label "2_0"
				state 50
				conservation "1 0 "
			]

			edge [
				source 1
				target 2
				state 50
				in_cluster 0
				conservation_rnaseq 0
				conservation "9 0 "
			]

			edge [
				source 2
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0
				conservation "10 0 "
			]

			edge [
				source 1
				target 4
				state 50
				in_cluster 0
				conservation_rnaseq 0
				conservation "1 0 "
			]

			edge [
				source 4
				target 2
				state 50
				in_cluster 0
				conservation_rnaseq 0
				conservation "1 0 "
			]

	]
