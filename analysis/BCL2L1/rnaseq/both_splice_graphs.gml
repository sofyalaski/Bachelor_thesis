
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
				label "1_1"
				state 0
				conservation "10 4 "
			]

			node [
				id 3
				label "1_2"
				state 50
				conservation "10 0 "
			]

			node [
				id 4
				label "1_3"
				state 0
				conservation "10 1 "
			]

			node [
				id 5
				label "1_4"
				state 50
				conservation "10 0 "
			]

			node [
				id 6
				label "1_5"
				state 0
				conservation "10 3 "
			]

			node [
				id 7
				label "2_0"
				state 0
				conservation "10 3 "
			]

			node [
				id 8
				label "stop"
				state 50
				conservation "10 0 "
			]

			node [
				id 9
				label "1_0"
				state 50
				conservation "2 0 "
			]

			node [
				id 10
				label "3_0"
				state 0
				conservation "2 1 "
			]

			node [
				id 11
				label "1_6"
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
				conservation "10 0 "
			]

			edge [
				source 3
				target 4
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 4
				target 5
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 5
				target 6
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 6
				target 7
				state 0
				in_cluster 0
				conservation_rnaseq 2.2222222222222223
				conservation "10 2 "
			]

			edge [
				source 7
				target 8
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "10 0 "
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
				target 9
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 9
				target 2
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 10
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 10
				target 4
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "1 1 "
			]

			edge [
				source 10
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 6
				target 11
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 11
				target 8
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 4
				target 6
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

	]
