function dirfis = create_fis(X, y, radii, dirsave)
dirfis = '';
options = genfisOptions('SubtractiveClustering');
options.AcceptRatio = radii;
fismat = genfis(X,y,options);
if exist('dirsave', 'var') && ~isempty(dirsave)
    writefis(fismat, dirsave);
    dirfis = dirsave;
end
end