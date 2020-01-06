
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
				label "1_2"
				state 0
				conservation "9 7 "
			]

			node [
				id 3
				label "8_0"
				state 0
				conservation "10 8 "
			]

			node [
				id 4
				label "10_0"
				state 0
				conservation "10 9 "
			]

			node [
				id 5
				label "9_0"
				state 0
				conservation "10 9 "
			]

			node [
				id 6
				label "6_0"
				state 0
				conservation "10 9 "
			]

			node [
				id 7
				label "5_0"
				state 0
				conservation "10 6 "
			]

			node [
				id 8
				label "5_1"
				state 0
				conservation "10 6 "
			]

			node [
				id 9
				label "3_0"
				state 0
				conservation "10 6 "
			]

			node [
				id 10
				label "3_1"
				state 50
				conservation "4 0 "
			]

			node [
				id 11
				label "12_0"
				state 0
				conservation "10 9 "
			]

			node [
				id 12
				label "4_0"
				state 0
				conservation "10 9 "
			]

			node [
				id 13
				label "7_0"
				state 0
				conservation "10 9 "
			]

			node [
				id 14
				label "2_0"
				state 0
				conservation "10 6 "
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
				label "1_1"
				state 50
				conservation "2 0 "
			]

			node [
				id 18
				label "8_1"
				state 0
				conservation "5 3 "
			]

			node [
				id 19
				label "13_0"
				state 50
				conservation "1 0 "
			]

			node [
				id 20
				label "0_2"
				state 50
				conservation "1 0 "
			]

			node [
				id 21
				label "1_0"
				state 50
				conservation "1 0 "
			]

			node [
				id 22
				label "12_1"
				state 0
				conservation "1 1 "
			]

			node [
				id 23
				label "14_0"
				state 0
				conservation "1 1 "
			]

			node [
				id 24
				label "15_0"
				state 0
				conservation "1 1 "
			]

			node [
				id 25
				label "11_0"
				state 0
				conservation "1 1 "
			]

			node [
				id 26
				label "9_1"
				state 0
				conservation "1 1 "
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
				conservation_rnaseq 4.444444444444445
				conservation "6 4 "
			]

			edge [
				source 4
				target 5
				state 0
				in_cluster 0
				conservation_rnaseq 8.88888888888889
				conservation "10 8 "
			]

			edge [
				source 5
				target 6
				state 0
				in_cluster 0
				conservation_rnaseq 8.88888888888889
				conservation "10 8 "
			]

			edge [
				source 6
				target 7
				state 0
				in_cluster 0
				conservation_rnaseq 5.555555555555555
				conservation "10 5 "
			]

			edge [
				source 7
				target 8
				state 0
				in_cluster 1
				conservation_rnaseq 6.0
				conservation "10 6 "
			]

			edge [
				source 8
				target 9
				state 0
				in_cluster 0
				conservation_rnaseq 5.555555555555555
				conservation "10 5 "
			]

			edge [
				source 9
				target 10
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "4 0 "
			]

			edge [
				source 10
				target 11
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "3 0 "
			]

			edge [
				source 11
				target 12
				state 0
				in_cluster 0
				conservation_rnaseq 8.88888888888889
				conservation "10 8 "
			]

			edge [
				source 12
				target 13
				state 0
				in_cluster 0
				conservation_rnaseq 8.88888888888889
				conservation "10 8 "
			]

			edge [
				source 13
				target 14
				state 0
				in_cluster 0
				conservation_rnaseq 5.555555555555555
				conservation "10 5 "
			]

			edge [
				source 14
				target 15
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 9
				target 11
				state 0
				in_cluster 0
				conservation_rnaseq 5.555555555555555
				conservation "7 5 "
			]

			edge [
				source 1
				target 16
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 16
				target 17
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 17
				target 2
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 2
				target 18
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 18
				target 4
				state 0
				in_cluster 0
				conservation_rnaseq 3.333333333333333
				conservation "5 3 "
			]

			edge [
				source 7
				target 19
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 19
				target 9
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 1
				target 20
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 20
				target 17
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 3
				target 18
				state 0
				in_cluster 1
				conservation_rnaseq 3.0
				conservation "4 3 "
			]

			edge [
				source 1
				target 21
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 21
				target 17
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
				source 10
				target 22
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 22
				target 12
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "1 1 "
			]

			edge [
				source 13
				target 23
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "1 1 "
			]

			edge [
				source 23
				target 15
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 13
				target 24
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 24
				target 25
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "1 1 "
			]

			edge [
				source 25
				target 26
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "1 1 "
			]

			edge [
				source 26
				target 15
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "1 0 "
			]

			edge [
				source 4
				target 6
				state 100
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "0 1 "
			]

			edge [
				source 2
				target 4
				state 100
				in_cluster 0
				conservation_rnaseq 2.2222222222222223
				conservation "0 2 "
			]

			edge [
				source 9
				target 12
				state 100
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "0 1 "
			]

			edge [
				source 3
				target 5
				state 100
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "0 1 "
			]

	]
