
[rDf, cDf] = size(df);
[rCenters, cCenters] = size(centers);

x = 1;
output_layer1 = zeros(rCenters, cCenters, rDf);
for i=1:rDf
    for j=1:cCenters
       for k=1:rCenters
           output_layer1(k,j,i) = gaussmf( df(i,j), [sigmas(j), centers(k,j) ] );
       end
    end
end