import time, torch
from model_arch import QPPNet
from train_utils import create_dataset, sample_data
import argparse


parser = argparse.ArgumentParser(description='QPPNet Arg Parser')

# Environment arguments
# required
parser.add_argument('-dir', '--save_dir', type=str, default='./saved_model',
                    help='Dir to save model weights (default: ./saved_model)')

parser.add_argument('--lr', type=float, default=1e-3,
                    help='Learning rate (default: 1e-3)')

parser.add_argument('--batch_size', type=int, default=32,
                    help='Batch size used in training (default: 32)')

parser.add_argument('-s', '--start_epoch', type=int, default=0,
                    help='Epoch to start training with (default: 0)')

parser.add_argument('-t', '--end_epoch', type=int, default=20,
                    help='Epoch to end training (default: 200)')
parser.add_argument('--save_latest_freq', type=int, default=500)                


if __name__ == '__main__':
    opt = parser.parse_args([])
    data_dir = 'res_by_temp/'
    dataset = create_dataset(data_dir)
    dataset_size = len(dataset)
    torch.set_default_tensor_type(torch.FloatTensor)
    qpp = QPPNet(opt)

    total_iter = 0

    for epoch in range(opt.start_epoch, opt.end_epoch):
        epoch_start_time = time.time()  # timer for entire epoch
        iter_data_time = time.time()    # timer for data loading per iteration
        epoch_iter = 0                  # the number of training iterations in current epoch, reset to 0 every epoch

        samp_dicts = sample_data(dataset, opt.batch_size)
        total_iter += opt.batch_size

        qpp.set_input(samp_dicts)
        qpp.optimize_parameters(opt.batch_size)

        #if total_iters % opt.print_freq == 0:    # print training losses and save logging information to the disk
        losses = qpp.get_current_losses()
        loss_str = "losses: "
        for op in losses:
          loss_str += str(op) + " [" + str(losses[op]) + "]; "
        print(loss_str)
        
        
        if total_iter % opt.save_latest_freq == 0:   # cache our latest model every <save_latest_freq> iterations
            print('saving the latest model (epoch %d, total_iters %d)' % (epoch, total_iter))
            qpp.save_units(epoch)