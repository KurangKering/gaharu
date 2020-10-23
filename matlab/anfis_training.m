dcsv = csvread('datalatih_10%_uji_normalisasi.csv');
epoch = 100;
opt(1) = epoch;
fis = readfis('matlab/10persen');
[trnfismat, rmse] = anfis(dcsv, fis, opt);
outputlatih = round(evalfis(dcsv(:,1:end-1),trnfismat));
errorlatih = numel(find(outputlatih ~= dcsv(:,end)));
duji = csvread('datauji_10%_uji_normalisasi.csv');
outputuji = round(evalfis(duji(:,1:end-1),trnfismat));
erroruji = numel(find(outputuji ~= duji(:,end)));
erroruji