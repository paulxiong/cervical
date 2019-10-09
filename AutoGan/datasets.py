import torch
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import Dataset


class ImageDataset(object):
    def __init__(self, args):
        if args.dataset.lower() == 'cifar10':
            Dt = datasets.CIFAR10          
            transform = transforms.Compose([
                transforms.Resize(args.img_size),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ])
            args.n_classes = 1
        elif args.dataset.lower() == 'stl10':
            Dt = datasets.STL10
            transform = transforms.Compose([
                transforms.Resize(args.img_size),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ])
        else:
            raise NotImplementedError('Unknown dataset: {}'.format(args.dataset))

        if args.dataset.lower() == 'stl10':
            self.train = torch.utils.data.DataLoader(
                Dt(root=args.data_path, split='train+unlabeled', transform=transform, download=True),
                batch_size=args.dis_batch_size, shuffle=True,
                num_workers=args.num_workers, pin_memory=True)

            self.valid = torch.utils.data.DataLoader(
                Dt(root=args.data_path, split='test', transform=transform),
                batch_size=args.dis_batch_size, shuffle=False,
                num_workers=args.num_workers, pin_memory=True)

            self.test = self.valid
        else:
            print("data_path:",args.data_path)
            Dt2 = Dt(root=args.data_path, train=True, transform=transform, download=True)
            Dt1 = Dt(root=args.data_path, train=False, transform=transform)          
            print("Dt_type:",type(Dt2))
            print("Dt:",Dt2)         
            print("Dt1_type:",type(Dt1))
            print("Dt1:",Dt1)
                     
            self.train = torch.utils.data.DataLoader(
                Dt2,
                batch_size=args.dis_batch_size, shuffle=True,
                num_workers=args.num_workers, pin_memory=True)
            print("self.train_type:",type(self.train))
            print("self.train",self.train)
            self.valid = torch.utils.data.DataLoader(
                Dt1,
                batch_size=args.dis_batch_size, shuffle=False,
                num_workers=args.num_workers, pin_memory=True)

            self.test = self.valid
            
class ImageDataset1(object):
    def __init__(self, args):
        if args.dataset.lower() == 'cifar10':
          #  Dt = datasets.CIFAR10
           # Dt = datasets.ImageNet('./data1',train=True, transform=transform, download=True )
            transform = transforms.Compose([
                transforms.Resize(args.img_size),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ])
            Dt = datasets.ImageFolder('./data1')
            args.n_classes = 2
        elif args.dataset.lower() == 'stl10':
            Dt = datasets.STL10
            transform = transforms.Compose([
                transforms.Resize(args.img_size),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ])
        else:
            raise NotImplementedError('Unknown dataset: {}'.format(args.dataset))

        if args.dataset.lower() == 'stl10':
            self.train = torch.utils.data.DataLoader(
                Dt(root=args.data_path, split='train+unlabeled', transform=transform, download=True),
                batch_size=args.dis_batch_size, shuffle=True,
                num_workers=args.num_workers, pin_memory=True)

            self.valid = torch.utils.data.DataLoader(
                Dt(root=args.data_path, split='test', transform=transform),
                batch_size=args.dis_batch_size, shuffle=False,
                num_workers=args.num_workers, pin_memory=True)

            self.test = self.valid
        else:
            print("data_path:",args.data_path)
            Dt2 = Dt(root=args.data_path, train=True, transform=transform, download=True)
            Dt1 = Dt(root=args.data_path, train=False, transform=transform)
            
            print("Dt_type:",type(Dt2))
            print("Dt:",Dt2)
            
            print("Dt1_type:",type(Dt1))
            print("Dt1:",Dt1)
            
            
            self.train = torch.utils.data.DataLoader(
                Dt2,
                batch_size=args.dis_batch_size, shuffle=True,
                num_workers=args.num_workers, pin_memory=True)
            print("self.train_type:",type(self.train))
            print("self.train",self.train)
            self.valid = torch.utils.data.DataLoader(
                Dt1,
                batch_size=args.dis_batch_size, shuffle=False,
                num_workers=args.num_workers, pin_memory=True)

            self.test = self.valid
            
            
            
            
            
            