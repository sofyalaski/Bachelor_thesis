
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
				label "3_0"
				state 0
				conservation "9 7 "
			]

			node [
				id 3
				label "2_0"
				state 0
				conservation "10 8 "
			]

			node [
				id 4
				label "13_0"
				state 0
				conservation "9 7 "
			]

			node [
				id 5
				label "6_0"
				state 0
				conservation "9 7 "
			]

			node [
				id 6
				label "8_0"
				state 0
				conservation "9 7 "
			]

			node [
				id 7
				label "10_0"
				state 0
				conservation "9 3 "
			]

			node [
				id 8
				label "10_1"
				state 0
				conservation "9 6 "
			]

			node [
				id 9
				label "11_0"
				state 0
				conservation "9 6 "
			]

			node [
				id 10
				label "4_0"
				state 0
				conservation "9 7 "
			]

			node [
				id 11
				label "9_0"
				state 0
				conservation "9 7 "
			]

			node [
				id 12
				label "7_1"
				state 0
				conservation "9 7 "
			]

			node [
				id 13
				label "5_0"
				state 0
				conservation "9 7 "
			]

			node [
				id 14
				label "1_0"
				state 0
				conservation "9 4 "
			]

			node [
				id 15
				label "stop"
				state 50
				conservation "10 0 "
			]

			node [
				id 16
				label "0_1"
				state 50
				conservation "1 0 "
			]

			node [
				id 17
				label "8_1"
				state 50
				conservation "1 0 "
			]

			node [
				id 18
				label "12_0"
				state 50
				conservation "1 0 "
			]

			node [
				id 19
				label "7_0"
				state 50
				conservation "1 0 "
			]

			edge [
				source 1
				target 2
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "9 0 "
			]

			edge [
				source 2
				target 3
				state 0
				in_cluster 0
				conservation_rnaseq 3.333333333333333
				conservation "9 3 "
			]

			edge [
				source 3
				target 4
				state 0
				in_cluster 0
				conservation_rnaseq 6.666666666666666
				conservation "9 6 "
			]

			edge [
				source 4
				target 5
				state 0
				in_cluster 0
				conservation_rnaseq 6.666666666666666
				conservation "9 6 "
			]

			edge [
				source 5
				target 6
				state 0
				in_cluster 0
				conservation_rnaseq 6.666666666666666
				conservation "9 6 "
			]

			edge [
				source 6
				target 7
				state 0
				in_cluster 0
				conservation_rnaseq 3.333333333333333
				conservation "9 3 "
			]

			edge [
				source 7
				target 8
				state 0
				in_cluster 1
				conservation_rnaseq 3.0
				conservation "8 3 "
			]

			edge [
				source 8
				target 9
				state 0
				in_cluster 0
				conservation_rnaseq 5.555555555555555
				conservation "9 5 "
			]

			edge [
				source 9
				target 10
				state 0
				in_cluster 0
				conservation_rnaseq 5.555555555555555
				conservation "9 5 "
			]

			edge [
				source 10
				target 11
				state 0
				in_cluster 0
				conservation_rnaseq 6.666666666666666
				conservation "9 6 "
			]

			edge [
				source 11
				target 12
				state 0
				in_cluster 0
				conservation_rnaseq 6.666666666666666
				conservation "9 6 "
			]

			edge [
				source 12
				target 13
				state 0
				in_cluster 0
				conservation_rnaseq 6.666666666666666
				conservation "9 6 "
			]

			edge [
				source 13
				target 14
				state 0
				in_cluster 0
				conservation_rnaseq 4.444444444444445
				conservation "9 4 "
			]

			edge [
				source 14
				target 15
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "9 0 "
			]

			edge [
				source 3
				target 16
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 16
				target 15
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

			edge [
				source 7
				target 17
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 17
				target 18
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 18
				target 19
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 19
				target 8
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 10
				target 12
				state 100
				in_cluster 0
				conservation_rnaseq 2.2222222222222223
				conservation "0 2 "
			]

			edge [
				source 11
				target 13
				state 100
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "0 1 "
			]

	]
