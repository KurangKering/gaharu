radii = 0.5;
radii = radii * ones(1,3);
accumMultp = 1.0 ./ radii;
numPoints = 3;
new_accumMultp = accumMultp(ones(1,numPoints),:);
hasil = zeros(1,3);
for i=1:numPoints
	thePoint = norm(i,:);
	thePoint = thePoint(ones(1,numPoints),:);
	dx = (thePoint - norm) .* new_accumMultp;
	hasil(i) = sum(exp(-4*sum(dx.^2,2)));
end
