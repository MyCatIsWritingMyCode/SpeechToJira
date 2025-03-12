import logging, re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer
#from bertopic import BERTopic
from models.app_config import *


class NLPProcessor:
    def __init__(self, logger : logging.Logger, config : Config):
        self.logger = logger
        self.config = config

        try:
            #self.topic_model = BERTopic.load("MaartenGr/BERTopic_Wikipedia")
            self.topic_model = SentenceTransformer("all-mpnet-base-v2")
            #self.nlp_model = pipeline("text-classification", model = config.model_config.topic_seg)
            self.logger.info(f"Initialized BERTopic model: {config.model_config.topic_seg}")
        except Exception as e:
            self.logger.error(f"Failed to initialize NLP processor model: {e}")
            raise

    def extract_topics(self, text : str) -> list[str]:
        try:

            #text_segments = self.__split_into_chunks(text, 200)
            sentences = re.split(r'(?<=[.!?]) +', text.strip())
            embeddings = self.topic_model.encode(sentences)
            # similarities = self.topic_model.similarity(embeddings, embeddings)
            # for idx_i, sentence1 in enumerate(sentences):
            #     print(sentence1)
            #     for idx_j, sentence2 in enumerate(sentences):
            #         print(f" - {sentence2: <30}: {similarities[idx_i][idx_j]:.4f}")

            similarities = [cosine_similarity([embeddings[i]], [embeddings[i+1]])[0][0]
                            for i in range(len(embeddings)-1)]

            segmented_text = self._cusum(similarities, sentences)

            resulting_segments : list[str] = []

            for key, string_list in segmented_text.items():
                if len(string_list) >= 2:
                    concatenated = ' '.join(string_list)
                    resulting_segments.append(concatenated)

            # for segment in segmented_text:
            #     print(f"Section {segment}: {segmented_text[segment]}")

            return resulting_segments

        except Exception as e:
            self.logger.error(f"Topic extraction failed: {e}")
            raise Exception(e)

    def _cusum(self, similarities, sentences) -> dict[int, list[str]]:
        """
        Simple one-sided CUSUM algorithm for detecting upward shifts.

        Parameters:
            similarities : Sequence of np.float32 values.
            sentences : Collection of sentences.

        Returns:
            section_dictionary : Dictionary of sections.
        """
        threshold : float = 0.2
        cumulative_sum : float = 0.0
        cumulative_sums : list[str] = []
        section_dictionary : dict[int, list[str]] = {}
        counter : int = 0
        current_collection : list[int] = []
        for i, x in enumerate(similarities):
            cumulative_sum = cumulative_sum + x
            cumulative_sums.append(cumulative_sum)
            if cumulative_sum > threshold:
                current_collection.append(sentences[i])
                cumulative_sum = 0  # Reset the cumulative sum after detection
            else:
                section_dictionary[counter] = current_collection
                current_collection = []
                counter += 1
        return section_dictionary