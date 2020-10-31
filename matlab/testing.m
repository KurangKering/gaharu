function [predicted] = testing(duji, dirfis)
fis = readfis(dirfis);
predicted = abs(round(evalfis(duji, fis)));
end