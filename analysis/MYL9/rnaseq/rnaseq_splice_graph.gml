
	graph [
		directed 1
		id 42
		label "splice graph of orthologous exon groups"

			node [
				id 1
				label "1_2"
				conservation 8
			]

			node [
				id 2
				label "1_3"
				conservation 9
			]

			node [
				id 3
				label "1_1"
				conservation 8
			]

			node [
				id 4
				label "1_4"
				conservation 9
			]

			edge [
				source 3
				target 1
				conservation 7.777777777777778
				in_cluster 0
			]

			edge [
				source 3
				target 4
				conservation 5.555555555555555
				in_cluster 0
			]

			edge [
				source 2
				target 4
				conservation 8.88888888888889
				in_cluster 0
			]

			edge [
				source 1
				target 2
				conservation 8.0
				in_cluster 1
			]

	]
