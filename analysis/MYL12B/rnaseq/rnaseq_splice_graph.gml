
	graph [
		directed 1
		id 42
		label "splice graph of orthologous exon groups"

			node [
				id 1
				label "3_0"
				conservation 6
			]

			node [
				id 2
				label "1_0"
				conservation 6
			]

			node [
				id 3
				label "2_0"
				conservation 3
			]

			edge [
				source 2
				target 1
				conservation 3.333333333333333
				in_cluster 0
			]

			edge [
				source 1
				target 3
				conservation 3.333333333333333
				in_cluster 0
			]

			edge [
				source 2
				target 3
				conservation 1.1111111111111112
				in_cluster 0
			]

	]
