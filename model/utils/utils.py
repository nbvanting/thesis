import matplotlib.pyplot as plt

def plot_training(history, title):
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]
    
    epochs = range(len(loss))
    
    plt.figure()
    plt.plot(epochs, loss, "b", label="Training loss")
    plt.plot(epochs, val_loss, "ro-", label="Validation loss")
    plt.title(title)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()

