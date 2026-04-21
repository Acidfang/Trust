"""
UPFM Field Solver
Solves: ∂i/∂t = -∇Φ(x,y) via gradient descent until convergence.

Each image IS the converged field state from solving this equation.
"""

import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt


class FieldSolver:
    """Solves gradient descent equation for UPFM image generation."""
    
    def __init__(self, grid_size=512, domain=(-3, 3), verbose=True):
        """
        Initialize solver on 2D grid.
        
        Args:
            grid_size: Number of points per dimension
            domain: (xmin, xmax) for domain
            verbose: Print convergence info
        """
        self.grid_size = grid_size
        self.domain = domain
        self.verbose = verbose
        
        # Create coordinate grid
        self.x = np.linspace(domain[0], domain[1], grid_size)
        self.y = np.linspace(domain[0], domain[1], grid_size)
        self.XX, self.YY = np.meshgrid(self.x, self.y)
        
        self.dx = self.x[1] - self.x[0]
        self.dy = self.y[1] - self.y[0]
    
    def solve(self, potential_func, t_max=500, dt=0.01, epsilon=1e-5, 
              init_scale=0.1, seed=42):
        """
        Solve gradient descent until convergence.
        
        ∂i/∂t = -∇Φ(x,y)
        
        Args:
            potential_func: Callable Φ(x, y) returning 2D array
            t_max: Maximum number of time steps
            dt: Time step size
            epsilon: Convergence threshold
            init_scale: Initial field noise magnitude
            seed: Random seed for reproducibility
        
        Returns:
            i_final: Converged field (complex for phase information)
        """
        np.random.seed(seed)
        
        # Compute potential once
        if self.verbose:
            print("Computing potential field...")
        Phi = potential_func(self.XX, self.YY)
        
        # Initialize field with small random noise
        if self.verbose:
            print("Initializing field...")
        i = np.random.randn(self.grid_size, self.grid_size) * init_scale
        i = i + 1j * np.random.randn(self.grid_size, self.grid_size) * init_scale
        
        # Time-stepping loop
        if self.verbose:
            print(f"Solving (max {t_max} steps)...")
        
        for t in range(t_max):
            # Compute gradient of potential
            dPhi_dy, dPhi_dx = np.gradient(Phi, self.dy, self.dx)
            
            # Compute gradient magnitude for convergence check
            grad_mag = np.sqrt(dPhi_dx**2 + dPhi_dy**2)
            max_grad = np.max(grad_mag)
            
            # Update field: i_{t+1} = i_t - dt * ∇Φ
            # Use complex representation: real and imag parts evolve independently
            i_real = np.real(i)
            i_imag = np.imag(i)
            
            i_real = i_real - dt * dPhi_dx
            i_imag = i_imag - dt * dPhi_dy
            
            i = i_real + 1j * i_imag
            
            # Check convergence
            if t % 50 == 0 or t < 10:
                if self.verbose:
                    print(f"  Step {t:4d}: max(∇Φ) = {max_grad:.6e}")
            
            if max_grad < epsilon:
                if self.verbose:
                    print(f"✓ Converged at step {t}")
                break
        
        if self.verbose:
            print(f"Final field magnitude range: [{np.min(np.abs(i)):.4f}, {np.max(np.abs(i)):.4f}]")
        
        return i, Phi


class GradientFieldSolver(FieldSolver):
    """Specialized solver that also tracks gradient field evolution."""
    
    def solve_with_gradient_tracking(self, potential_func, t_max=500, dt=0.01, 
                                     epsilon=1e-5, init_scale=0.1):
        """Solve and return both field and its gradient for visualization."""
        i, Phi = self.solve(potential_func, t_max, dt, epsilon, init_scale)
        
        # Compute gradient of converged field
        di_dy, di_dx = np.gradient(np.abs(i), self.dy, self.dx)
        
        return i, Phi, di_dx, di_dy


# Example usage and testing
if __name__ == "__main__":
    
    # Test: Simple Gaussian potential
    def gaussian_potential(x, y, sigma=0.5):
        """Simple 2D Gaussian potential."""
        return np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    solver = FieldSolver(grid_size=256, domain=(-3, 3))
    i, Phi = solver.solve(gaussian_potential, t_max=300, dt=0.01)
    
    # Plot results
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Potential
    axes[0].imshow(Phi, extent=solver.domain+solver.domain, cmap='RdBu')
    axes[0].set_title('Potential Φ(x,y)')
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('y')
    plt.colorbar(axes[0].images[0], ax=axes[0])
    
    # Field magnitude
    axes[1].imshow(np.abs(i), extent=solver.domain+solver.domain, cmap='hot')
    axes[1].set_title('Converged Field |i|')
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('y')
    plt.colorbar(axes[1].images[0], ax=axes[1])
    
    plt.tight_layout()
    plt.savefig('c:\\Determined\\test_solver.png', dpi=150, bbox_inches='tight')
    print("Test plot saved: test_solver.png")
