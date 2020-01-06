
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
				label "0_1"
				state 50
				conservation "2 0 "
			]

			node [
				id 3
				label "1_3"
				state 0
				conservation "10 6 "
			]

			node [
				id 4
				label "3_0"
				state 0
				conservation "10 2 "
			]

			node [
				id 5
				label "3_1"
				state 50
				conservation "10 0 "
			]

			node [
				id 6
				label "3_2"
				state 50
				conservation "10 0 "
			]

			node [
				id 7
				label "3_3"
				state 50
				conservation "10 0 "
			]

			node [
				id 8
				label "3_4"
				state 0
				conservation "10 3 "
			]

			node [
				id 9
				label "2_0"
				state 0
				conservation "10 3 "
			]

			node [
				id 10
				label "2_1"
				state 50
				conservation "10 0 "
			]

			node [
				id 11
				label "2_2"
				state 0
				conservation "10 2 "
			]

			node [
				id 12
				label "4_0"
				state 0
				conservation "10 2 "
			]

			node [
				id 13
				label "4_1"
				state 0
				conservation "10 2 "
			]

			node [
				id 14
				label "4_2"
				state 50
				conservation "8 0 "
			]

			node [
				id 15
				label "2_3"
				state 0
				conservation "10 4 "
			]

			node [
				id 16
				label "stop"
				state 50
				conservation "10 0 "
			]

			node [
				id 17
				label "2_4"
				state 0
				conservation "6 1 "
			]

			node [
				id 18
				label "1_1"
				state 50
				conservation "6 0 "
			]

			node [
				id 19
				label "1_2"
				state 0
				conservation "6 1 "
			]

			node [
				id 20
				label "1_0"
				state 0
				conservation "2 1 "
			]

			node [
				id 21
				label "4_3"
				state 50
				conservation "6 0 "
			]

			node [
				id 22
				label "1_4"
				state 0
				conservation "2 1 "
			]

			node [
				id 23
				label "0_2"
				state 50
				conservation "2 0 "
			]

			node [
				id 24
				label "0_3"
				state 50
				conservation "2 0 "
			]

			node [
				id 25
				label "0_4"
				state 50
				conservation "2 0 "
			]

			node [
				id 26
				label "0_5"
				state 50
				conservation "2 0 "
			]

			node [
				id 27
				label "0_6"
				state 50
				conservation "2 0 "
			]

			node [
				id 28
				label "5_0"
				state 0
				conservation "2 1 "
			]

			node [
				id 29
				label "0_7"
				state 50
				conservation "2 0 "
			]

			node [
				id 30
				label "0_8"
				state 50
				conservation "2 0 "
			]

			node [
				id 31
				label "6_0"
				state 0
				conservation "2 1 "
			]

			node [
				id 32
				label "0_10"
				state 0
				conservation "2 1 "
			]

			node [
				id 33
				label "0_9"
				state 50
				conservation "2 0 "
			]

			node [
				id 34
				label "0_11"
				state 0
				conservation "2 1 "
			]

			edge [
				source 1
				target 2
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 2
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 3
				target 4
				state 0
				in_cluster 0
				conservation_rnaseq 2.2222222222222223
				conservation "10 2 "
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
				state 0
				in_cluster 0
				conservation_rnaseq 2.2222222222222223
				conservation "10 2 "
			]

			edge [
				source 9
				target 10
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 10
				target 11
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 11
				target 12
				state 0
				in_cluster 0
				conservation_rnaseq 2.2222222222222223
				conservation "10 2 "
			]

			edge [
				source 12
				target 13
				state 0
				in_cluster 1
				conservation_rnaseq 2.0
				conservation "10 2 "
			]

			edge [
				source 13
				target 14
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "8 0 "
			]

			edge [
				source 14
				target 15
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "6 0 "
			]

			edge [
				source 15
				target 16
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "10 0 "
			]

			edge [
				source 1
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 14
				target 17
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "4 0 "
			]

			edge [
				source 17
				target 16
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "6 0 "
			]

			edge [
				source 1
				target 18
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "4 0 "
			]

			edge [
				source 18
				target 19
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "6 0 "
			]

			edge [
				source 19
				target 3
				state 0
				in_cluster 1
				conservation_rnaseq 1.0
				conservation "6 1 "
			]

			edge [
				source 6
				target 8
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 20
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 20
				target 19
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "2 1 "
			]

			edge [
				source 13
				target 17
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "2 1 "
			]

			edge [
				source 13
				target 15
				state 0
				in_cluster 0
				conservation_rnaseq 2.2222222222222223
				conservation "4 2 "
			]

			edge [
				source 20
				target 18
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 14
				target 21
				state 50
				in_cluster 1
				conservation_rnaseq 0.0
				conservation "6 0 "
			]

			edge [
				source 21
				target 16
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "6 0 "
			]

			edge [
				source 20
				target 3
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "2 1 "
			]

			edge [
				source 13
				target 22
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "2 1 "
			]

			edge [
				source 22
				target 16
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 4
				target 9
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "2 1 "
			]

			edge [
				source 3
				target 9
				state 0
				in_cluster 0
				conservation_rnaseq 2.2222222222222223
				conservation "2 2 "
			]

			edge [
				source 1
				target 11
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 23
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 23
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 24
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 24
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 25
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 25
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 3
				target 6
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 26
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 26
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 27
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 27
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 14
				target 28
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 28
				target 16
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 29
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 29
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 30
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 30
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 9
				target 31
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 31
				target 32
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 32
				target 16
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 33
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 33
				target 3
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 1
				target 34
				state 50
				in_cluster 0
				conservation_rnaseq 0.0
				conservation "2 0 "
			]

			edge [
				source 34
				target 3
				state 0
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "2 1 "
			]

			edge [
				source 20
				target 4
				state 100
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "0 1 "
			]

			edge [
				source 3
				target 12
				state 100
				in_cluster 0
				conservation_rnaseq 1.1111111111111112
				conservation "0 1 "
			]

	]
