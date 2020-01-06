
	graph [
		directed 1
		id 42
		label "splice graph of orthologous exon groups"

			node [
				id 1
				label "1_1"
				conservation 4
			]

			node [
				id 2
				label "1_5"
				conservation 3
			]

			node [
				id 3
				label "1_3"
				conservation 1
			]

			node [
				id 4
				label "3_0"
				conservation 1
			]

			node [
				id 5
				label "2_0"
				conservation 3
			]

			edge [
				source 4
				target 3
				conservation 1.1111111111111112
				in_cluster 0
			]

			edge [
				source 2
				target 5
				conservation 2.2222222222222223
				in_cluster 0
			]

	]
