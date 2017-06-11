from data_wrangler import CustomDataWrangler
import config
from cnn import ElementClassifier
import numpy as np
import sklearn

def calculate_class_wise_metrics(dataset, num_samples):
	dw = CustomDataWrangler()
	cnn = ElementClassifier(config.NUM_CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
	cnn.load_model(config.MODEL_TO_LOAD)


	correct = np.zeros((config.NUM_CLASSES))
	true_positive = np.zeros((config.NUM_CLASSES))
	false_negative = np.zeros((config.NUM_CLASSES))
	false_positive = np.zeros((config.NUM_CLASSES))
	true_negative = np.zeros((config.NUM_CLASSES))
	samples = 0
	if dataset == "train":
		gen = dw.get_train_generator()
	else:
		gen = dw.get_val_generator()

	for x, actual in gen:
		pred = cnn.predict(x) > 0.50

		correct += np.sum(pred == actual, axis=0)

		#Calc true positives
		positive = pred.copy()
		batch_true_positives = np.zeros((config.BATCH_SIZE, config.NUM_CLASSES))
		batch_true_positives[actual == 1] = (positive == actual)[actual == 1]
		true_positive += np.sum(batch_true_positives, axis=0)

		#Calc false negatives
		positive = pred.copy()
		batch_false_negatives = np.zeros((config.BATCH_SIZE, config.NUM_CLASSES))
		batch_false_negatives[actual == 1] = (positive != actual)[actual == 1]
		false_negative += np.sum(batch_false_negatives, axis=0)

		#Calc false positives
		positive = pred.copy()
		batch_false_negatives = np.zeros((config.BATCH_SIZE, config.NUM_CLASSES))
		batch_false_negatives[actual == 0] = (positive != actual)[actual == 0]
		false_positive += np.sum(batch_false_negatives, axis=0)

		#Calc true negatives
		positive = pred.copy()
		batch_false_negatives = np.zeros((config.BATCH_SIZE, config.NUM_CLASSES))
		batch_false_negatives[actual == 0] = (positive == actual)[actual == 0]
		true_negative += np.sum(batch_false_negatives, axis=0)

		samples += actual.shape[0]
		print(samples)
		if samples >= num_samples:
			break

	accuracy = correct / samples
	true_positive /= samples
	false_negative /= samples
	false_positive /= samples
	true_negative /= samples
	recall = true_positive / (true_positive + false_negative)
	print(recall)
	precision = true_positive / (true_positive + false_positive)
	f1 = 2*((precision*recall)/(precision+recall))

	np.save("accuracy.npy", accuracy)
	np.save("recall.npy", recall)
	print("Accuracy:", sum(accuracy)/config.NUM_CLASSES)
	print("True positive:", sum(true_positive)/config.NUM_CLASSES)
	print("False positive:", sum(false_positive)/config.NUM_CLASSES)
	print("True negative:", sum(true_negative)/config.NUM_CLASSES)
	print("False negative:", sum(false_negative)/config.NUM_CLASSES)
	print("Recall:", sum(recall)/config.NUM_CLASSES)
	print("Precision:", sum(precision)/config.NUM_CLASSES)
	print("F1 score:", sum(f1)/config.NUM_CLASSES)
	return accuracy


if __name__ == "__main__":
	NUM_TRAIN_SAMPLES = 46197
	NUM_VAL_SAMPLES = 11528
	RECALCULATE = True
	DATASET = "val"

	if RECALCULATE:
		accuracy = calculate_class_wise_metrics(DATASET, NUM_VAL_SAMPLES)
	else:
		accuracy = np.load("accuracy.npy")
