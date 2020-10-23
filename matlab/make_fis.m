function dirfis = make_fis(X, y, radii, dirsave)
dirfis = '';
fismat = genfis2(X,y,radii);
if exist('dirsave', 'var') && ~isempty(dirsave)
    writefis(fismat, dirsave);
    dirfis = dirsave;
end
end