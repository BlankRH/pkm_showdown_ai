# Create your first MLP in Keras
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from keras.models import load_model
import numpy

class Evaluator():
    def __init__(self):
        self.early_stopping = EarlyStopping(monitor='val_loss', patience=10)

    def init(self):
        self.model = Sequential()
        try:
            self.model.load_model("data/model.hdf5", by_name=True)
        except:
            print("No avaliable model")
            dataset = numpy.loadtxt("data/diabetes.csv", delimiter=",")
            X = dataset[:,:8]
            Y = dataset[:,8]
            layer1 = Dense(2, input_dim=8, activation='relu')
            layer2 = Dense(4, activation='relu')
            layer3 = Dense(1, activation='sigmoid')
            model.add(layer1)
            model.add(layer2)
            model.add(layer3)
            self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'], verbose=False)
            self.model.fit(X, Y, epochs=100, batch_size=20, validation_split=0.2, callbacks=[early_stopping])
            self.model.save('data/model.hdf5')

    def train(self, l1=27, l2=28, l3=1, l4=1): #acc: 77.47%
        dataset = numpy.loadtxt("data/diabetes.csv", delimiter=",")
        X = dataset[:,:8]
        Y = dataset[:,8]
        #with open("data/model.hdf5", "w") as fp:
        #    fp.truncate()
        #TODO
        model = Sequential()
        layer1 = Dense(l1, input_dim=8, activation='relu')
        layer2 = Dense(l2, activation='relu')
        layer3 = Dense(l3, activation='relu')
        layer4 = Dense(l4, activation='sigmoid')
        model.add(layer1)
        model.add(layer2)
        model.add(layer3)
        model.add(layer4)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X, Y, epochs=150, batch_size=20, validation_split=0.2, callbacks=[self.early_stopping], verbose=0)
        scores = model.evaluate(X, Y)
        print("l1=%d, l2=%d, l3=%d, %s: %.2f%%" % (l1, l2, l3, model.metrics_names[1], scores[1]*100))
        with open("parameter.txt", "a") as fp:
            print("l1=%d, l2=%d, l3=%d, %s: %.2f%%" % (l1, l2, l3, model.metrics_names[1], scores[1]*100), file=fp)
        #self.model.save('data/model.hdf5')

    def predict(self, datapath="data/diabetes.csv"):
        init()
        dataset = numpy.loadtxt(datapath, delimiter=",")#change the path!!!
        X = dataset[:,:8]
        Y = dataset[:,8]
        preds = self.model.predict(X, batch_size=20)
        return preds

    def findMaxParameter(self):
        with open("parameter.txt") as fp:
            p = fp.readlines()
            maxacc = 0
            l1m = l2m = 0
            for line in p:
                accd = int(line[-4:-2])
                acci = int(line[-7:-5])
                acc = acci + accd * 0.01
                if acc > maxacc:
                    maxacc = acc
                    l1m = int(line[line.find('=')+1:line.find(',')])
                    l2m = int(line[line.find('=', line.find('=')+1)+1:line.find(',', line.find(',')+1)])
            print("l1={}, l2={}, ".format(l1m, l2m),end="")
            print("acc=", maxacc, "%",sep='')
#
if __name__ == '__main__':
    from argparse import ArgumentParser
    argparser = ArgumentParser()
    argparser.add_argument('--delete', type=bool, default=False)
    argparser.add_argument('--mode', default='train')
    args = argparser.parse_args()
    if args.delete:
        with open("data/model.hdf5", "w") as fp:
            fp.truncate()
    ev = Evaluator()
    if args.mode == 'train':
        with open("parameter.txt", "a") as fp:
            print("\n")
        for i in range(1,10):
            for j in range(1,10):
                for z in range(1, 10):
                    ev.train(l1=i, l2=j, l3=z)
        ev.findMaxParameter()
    elif args.mode == 'predict':
        ev.predict()
    else:
        print("Argument not avaliable")
