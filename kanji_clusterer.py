################################################################################################
#                                                                                              #
# kanji_clusterer.py                                                                           #
# The goal is to create some rough high-level kanji categories, maybe identify some radicals.  #
# To do so, a batch KMeans classificator is used and fed batches of 250x250 images of kanjis.  #
# A single image per kanji is used.                                                            #
# Afterward two types of models will be trained on the result:                                 #
#    1) A cluster classificator, replicating the KMeans classificator but using a cnn          #
#       and taking lower resolution images and more images (~60) for a single kanji.           #
#    2) An OCR CNN for each cluster.                                                           #
#                                                                                              #
################################################################################################
import os
import pickle
import uuid
from sklearn.cluster import KMeans, MiniBatchKMeans
import scipy
import config


def make_cluster_dirs(data_dir, n_clusters):
    "Creates directories for the clusters in the order top->cluster id->train/val. Useful to train individual models for each cluster."
    for i in range(n_clusters):
        directory = os.path.join(data_dir, str(i))
        train_dir = os.path.join(directory, "train")
        val_dir = os.path.join(directory, "val")
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(train_dir):
            os.makedirs(train_dir)
        if not os.path.exists(val_dir):
            os.makedirs(val_dir)

def make_cluster_dirs_reverse_order(data_dir, n_clusters):
    "Creates directories for the clusters in the order top->train/val->cluster id. Useful to train a model to classify clusters."
    train_dir = os.path.join(data_dir, "train")
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
        for i in range(n_clusters):
            directory = os.path.join(train_dir, str(i))
            if not os.path.exists(directory):
                os.makedirs(directory)

    val_dir = os.path.join(data_dir, "val")
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)
        for i in range(n_clusters):
            directory = os.path.join(val_dir, str(i))
            if not os.path.exists(directory):
                os.makedirs(directory)
    



if __name__ == "__main__":
    N_KANJIS = 3144
    N_CLUSTER = N_KANJIS // 20
    BATCH_SIZE = 1000
    DATA_DIR = "kanji_clusters"
    DATA_DIR2 = "kanji_clusters2"

    # Create dirs to store symbolic links to data in order to sort data by clusters.
    make_cluster_dirs(DATA_DIR, N_CLUSTER)
    make_cluster_dirs_reverse_order(DATA_DIR2, N_CLUSTER)
    
    kanjis = os.listdir(config.HD_VAL_DIR)

    def get_kanji_path(kanji):
        "Returns the path to the HD first image for the given kanji."
        image_name = os.listdir(os.path.join(config.HD_VAL_DIR, kanji))[0]
        return os.path.join(config.HD_VAL_DIR, kanji, image_name)

    def get_first_image(kanji):
        "Returns the first image found for given kanji in a numpy array."
        image_path = get_kanji_path(kanji)
        image = scipy.misc.imread(image_path, flatten=True)
        return image.flatten()

    KM = MiniBatchKMeans(n_clusters=N_CLUSTER, batch_size=BATCH_SIZE)
    kanji_batches = [kanjis[i:i+BATCH_SIZE] for i in range(0, len(kanjis), BATCH_SIZE)]

    # Train KMeans on batches of kanji images.
    i = 0
    for batch in kanji_batches:
        print("Batch:", i)
        im_batch = [get_first_image(kanji) for kanji in batch]
        KM.partial_fit(im_batch)
        i += 1
    
    # Empty dict to check how big each cluster is
    cluster_sizes = {}
    for n in range(N_CLUSTER): cluster_sizes[n] = 0

    # Gets the cluster prediction for each kanji and creates symbolic links to the data in the approriate cluster directories
    for kanji in kanjis:
        im = get_first_image(kanji)
        cluster = KM.predict(im.reshape(1, -1)) # Reshape necessary when feeding a single sample to KM.predict.
        cluster_sizes[cluster[0]] += 1

        # Create symlink for kanji dir in appropriate cluster dir for individual model training
        src = os.path.join(config.TRAIN_DIR, kanji)
        dest = os.path.join(DATA_DIR, str(cluster[0]), "train", kanji)
        os.symlink(os.path.abspath(src), os.path.abspath(dest))

        # Create symlinks for each kanji image in appropriate cluster dir for cluster classification
        for f in os.listdir(src):
            inner_src = os.path.join(src, f)
            dest = os.path.join(DATA_DIR2, "train", str(cluster[0]), str(uuid.uuid4()))
            os.symlink(os.path.abspath(inner_src), os.path.abspath(dest))

        # Same as above but for validation set
        src = os.path.join(config.VAL_DIR, kanji)
        dest = os.path.join(DATA_DIR, str(cluster[0]), "val", kanji)
        os.symlink(os.path.abspath(src), os.path.abspath(dest))

        for f in os.listdir(src):
            inner_src = os.path.join(src, f)
            dest = os.path.join(DATA_DIR2, "val", str(cluster[0]), str(uuid.uuid4()))
            os.symlink(os.path.abspath(inner_src), os.path.abspath(dest))

    for i in cluster_sizes:
        print(i)
        print(cluster_sizes[i])
        print("-----")

    # Saves cluster centers as images to check how good they are.
    for n in range(N_CLUSTER):
        center = KM.cluster_centers_[n, :]
        center = center.reshape(250, 250)
        scipy.misc.imsave(os.path.join('cluster_centers', str(n) + '.jpg'), center)

    # Saves the model to a file
    with open("models\\kmeans.pickle", "wb") as f:
        pickle.dump(KM, f, pickle.HIGHEST_PROTOCOL)
