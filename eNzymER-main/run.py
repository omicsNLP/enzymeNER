import argparse
import eNzymER_model as eNER

parser = argparse.ArgumentParser(prog='eNzymER')
parser.add_argument('-t', type=str,)
parser.add_argument('--wdEmbed', type=str,
                    default="SciBERT", help="or BioBERT")
parser.add_argument('--model', type=str,
                    default="SciModel", help="or BioModel")
parser.add_argument('--isTrain', type=bool, default=False)
parser.add_argument('--train_set', type=str,
                    default="./TrainingSet/TrainingSet.txt")
parser.add_argument('--train_annotset', type=str,
                    default="./TrainingSet/TrainingSetAnnot.txt")
parser.add_argument('--test_json', type=str,
                    default="eNzymER_SciModel.json", help="eNzymER_BioModel.json")
parser.add_argument('--pretrain_model', type=str, default="./SciBertModels/epoch_9_SciModel_weights",
                    help="./BioBertModels/epoch_9_BioModel_weights")
parser.add_argument('--test_set', type=str, default="./TestSet/test.txt",
                    help="./TestSet/test_exclude_abbre.txt")
parser.add_argument('--test_annotset', type=str, default="./TestSet/testAnnotated.txt",
                    help="./TestSet/testAnnotated_exclude_abbre.txt")


if __name__ == '__main__':

    args = parser.parse_args()
    em = eNER.eNzymER(args.wdEmbed)
    if args.isTrain:
        em.train(args.train_set, args.train_annotset, args.model)
    else:
        em.load(args.test_json, args.pretrain_model)
        em.test(args.test_set, args.test_annotset)
        res = em.process("By using MMP-14 transfection, 12-O-tetradecanoylphorbol-13-acetate stimulation, and MMPI blockade, we showed the dynamic nature of proteolytic shedding and that the accumulation of cleaved ectodomains and protein fragments was proteinase dependent, executed by the cell surface membrane type 1 matrix metalloproteinase, MMP-14.")
        print(res)
