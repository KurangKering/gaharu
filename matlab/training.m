function [rmse, stepSize] = training(dtrain, dirfis, epoch, dirsave)

warning('off');
opt = anfisOptions;
fis = readfis(dirfis);
opt.InitialFIS = fis;
opt.EpochNumber = epoch;
opt.DisplayANFISInformation = 0;
opt.DisplayErrorValues = 0;
opt.DisplayStepSize = 0;
opt.DisplayFinalResults = 0;
[outfis, rmse, stepSize] = anfis(dtrain, opt);
if exist('dirsave', 'var') && ~isempty(dirsave)
    writefis(outfis, dirsave);
end