
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
				state 0
				conservation "10 6 "
			]

			node [
				id 3
				label "3_0"
				state 0
				conservation "10 6 "
			]

			node [
				id 4
				label "2_0"
				state 0
				conservation "10 3 "
			]

			node [
				id 5
				label "stop"
				state 50
				conservation "10 0 "
			]

			edge [
				source 1
				target 2
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 2
				target 3
				state 0
				in_cluster 0
				conservation_rnaseq 3.333333333333333
				conservation "10 3 "
			]

			edge [
				source 3
				target 4
				state 0
				in_cluster 0
				conservation_rnaseq 3.333333333333333
				conservation "10 3 "
			]

			edge [
				source 4
				target 5
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 2
				target 4
				state 100
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "0 1 "
			]

	]
