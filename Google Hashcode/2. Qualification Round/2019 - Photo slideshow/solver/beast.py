from .basesolver import BaseSolver


class Solver(BaseSolver):
	"""Solve the problem nice and steady!

	!!! This class need to be named 'Solver', otherwise main.py won't find this class.
	"""

	def solve(self):
		"""Compute a solution to the given problem.

		Save everything in an internal state,
		print the calculated score of the solution.


		:return: True, if a solution is found, False otherwise
		"""
		number_of_buckets = 50
		tags = {}
		tag_bucket_dict = {}
		tags_in_bucket = {}
		img_in_buckets = {i:[] for i in range(number_of_buckets)}

		for img in self.images:
			for tg in img['tags']:
				if tg not in tags:
					tags[tg] = 0
				tags[tg] += 1

		i = 0
		for tag in tags:
			id = i % number_of_buckets
			tag_bucket_dict[tag] = id
			if id not in tags_in_bucket:
				tags_in_bucket[id] = []
			tags_in_bucket[id].append(tag)
			i+=1

		img_id = 0
		for img in self.images:
			best_score_so_far,best_bucket_so_far = 1000000000000,-1
			for bucked_id in tags_in_bucket:
				overlaps = 0
				for tag in img['tags']:
					if tag in tags_in_bucket[bucked_id]:
						overlaps += 1
				non_overlaps = abs(len(tags_in_bucket[bucked_id])-overlaps)

				score = abs(overlaps-non_overlaps)
				if score<best_score_so_far:
					best_score_so_far = score
					best_bucket_so_far = bucked_id


			img_in_buckets[best_bucket_so_far].append([img_id,img['orientation']])
			img_id += 1

		for bucket_id in img_in_buckets:
			img_in_buckets[bucket_id] = sorted(img_in_buckets[bucket_id],key=lambda x:x[1])
			buck = img_in_buckets[bucket_id]

			i = 0
			while i < len(buck):
				if buck[i][1] == 'H':
					self.slides.append([buck[i][0]])
				elif buck[i][1] == 'V':
					if i+1<len(buck):
						self.slides.append([buck[i][0],buck[i+1][0]])
						i+=1
				i+=1
		print(self.slides)
		#print(tags_in_bucket)
		#print(tag_bucket_dict)
		print(img_in_buckets)
		for tag in tags:
			print(tag)

		return False
