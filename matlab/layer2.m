[rOutput, cOutput, bOutput]= size(output_layer1);

output_layer2 = zeros(bOutput, rOutput);
for i=1:bOutput
    for j=1:rOutput
        output_layer2(i,j) = prod(output_layer1(j,:,i));
    end
end