import torch

# Create two tensors and tell PyTorch to track their gradients.
# This is necessary if we want to compute derivatives with respect
# to these tensors later.
a = torch.tensor([2., 3.], requires_grad=True)
b = torch.tensor([6., 4.], requires_grad=True)


# Define the function:
#
#     f = 3 * a^3 - b^2
#
# Since a and b are vectors, f is also a vector.
f = 3 * a**3 - b**2


# Compute the gradients using backpropagation.
#
# f contains multiple values, so we provide an incoming gradient
# of [1, 1]. This is equivalent to computing the gradient of:
#
#     f[0] + f[1]
#
# with respect to a and b.
f.backward(gradient=torch.tensor([1., 1.]))


# The gradients are stored in the .grad attribute.
print(a.grad)
print(b.grad)
