
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
				conservation "9 0 "
			]

			node [
				id 3
				label "1_1"
				state 0
				conservation "10 8 "
			]

			node [
				id 4
				label "1_2"
				state 0
				conservation "10 8 "
			]

			node [
				id 5
				label "1_3"
				state 0
				conservation "10 9 "
			]

			node [
				id 6
				label "1_4"
				state 0
				conservation "10 9 "
			]

			node [
				id 7
				label "1_5"
				state 50
				conservation "10 0 "
			]

			node [
				id 8
				label "1_6"
				state 50
				conservation "10 0 "
			]

			node [
				id 9
				label "stop"
				state 50
				conservation "10 0 "
			]

			node [
				id 10
				label "2_0"
				state 50
				conservation "1 0 "
			]

			edge [
				source 1
				target 2
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "8 0 "
			]

			edge [
				source 2
				target 3
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "9 0 "
			]

			edge [
				source 3
				target 4
				state 0
				in_cluster 1
				conservation_rnaseq 8.0
				conservation "10 8 "
			]

			edge [
				source 4
				target 5
				state 0
				in_cluster 1
				conservation_rnaseq 8.0
				conservation "10 8 "
			]

			edge [
				source 5
				target 6
				state 0
				in_cluster 1
				conservation_rnaseq 9.0
				conservation "10 9 "
			]

			edge [
				source 6
				target 7
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 7
				target 8
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 8
				target 9
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 3
				target 6
				state 0
				in_cluster 0
				conservation_rnaseq 5.555555555555555
				conservation "2 5 "
			]

			edge [
				source 4
				target 7
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 1
				target 10
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 10
				target 2
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 1
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

	]
