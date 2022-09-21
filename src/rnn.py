import pandas as pd
import tensorflow as tf


def load_data(file: str, label: str = None) -> pd.DataFrame:
    if label:  # Train
        return tf.data.experimental.make_csv_dataset(
            file_pattern=file,
            batch_size=16,
            label_name=label,
            select_columns=["text", label],
            num_epochs=1,
        )
    else:  # Test
        return tf.data.experimental.make_csv_dataset(
            file_pattern=file,
            batch_size=16,
            select_columns=["text"],
            num_epochs=1,
        )


if __name__ == "__main__":
    train_ds = load_data(file="data/cleaned_train.csv", label="target")
    test_ds = load_data(file="data/cleaned_test.csv")

    # Test
    for feature, label in train_ds.take(1):
        print("feature:")
        print(feature)
        print("label")
        print(label)

    for feature in test_ds.take(1):
        print("feature:")
        print(feature)
