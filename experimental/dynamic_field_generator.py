"""
DYNAMIC FIELD VISUALIZATION GENERATOR
Generate field visualizations on-demand for any field parameters

Can be called from:
- Web server (Flask/FastAPI)
- CLI with custom parameters
- Interactive notebook
- GitHub Actions workflow

Supports real-time parameter adjustment and cascade simulation
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from scipy.ndimage import gaussian_filter
from scipy.integrate import solve_ivp
import matplotlib.animation as animation
from io import BytesIO
import base64

class DynamicFieldGenerator:
    """Generate field visualizations with custom parameters"""
    
    def __init__(self, D=1.0, alpha=0.1, beta=0.01, domain_size=10, resolution=100):
        """
        Initialize field generator
        
        Parameters:
        - D: Diffusion coefficient (spatial spreading)
        - alpha: Linear response coefficient
        - beta: Nonlinear (cascade) coefficient
        - domain_size: Size of spatial domain
        - resolution: Grid points for simulation
        """
        self.D = D
        self.alpha = alpha
        self.beta = beta
        self.domain_size = domain_size
        self.resolution = resolution
        
        # Create grid
        self.x = np.linspace(0, domain_size, resolution)
        self.y = np.linspace(0, domain_size, resolution)
        self.X, self.Y = np.meshgrid(self.x, self.y)
    
    def solve_diffusion_equation(self, initial_conditions, t_span, t_eval):
        """
        Solve dρ/dt = D·∇²ρ + α·f_external + β·ρ²
        
        Uses finite difference method with forward Euler in time
        """
        dx = self.domain_size / (self.resolution - 1)
        dt = (t_span[1] - t_span[0]) / len(t_eval)
        
        rho = initial_conditions.copy()
        solutions = [rho.copy()]
        
        for t_step in range(len(t_eval) - 1):
            # Laplacian using finite differences (5-point stencil)
            lap_rho = np.zeros_like(rho)
            for i in range(1, self.resolution - 1):
                for j in range(1, self.resolution - 1):
                    lap_rho[i, j] = (
                        rho[i+1, j] + rho[i-1, j] + 
                        rho[i, j+1] + rho[i, j-1] - 
                        4 * rho[i, j]
                    ) / (dx**2)
            
            # Time step: dρ/dt = D·∇²ρ + α·ρ + β·ρ²
            drho_dt = self.D * lap_rho + self.alpha * rho + self.beta * rho**2
            
            rho = rho + dt * drho_dt
            
            # Boundary conditions (Dirichlet: rho=0 at boundaries)
            rho[0, :] = 0
            rho[-1, :] = 0
            rho[:, 0] = 0
            rho[:, -1] = 0
            
            solutions.append(rho.copy())
        
        return np.array(solutions)
    
    def generate_radial_field_simulation(self, output_file="radial_simulation.gif"):
        """Generate animated radial diffusion field"""
        
        # Initial Gaussian point source
        initial = np.exp(-((self.X - self.domain_size/2)**2 + (self.Y - self.domain_size/2)**2) / 1.0)
        
        # Solve PDE
        t_span = (0, 1.0)
        t_eval = np.linspace(0, 1.0, 20)
        solutions = self.solve_diffusion_equation(initial, t_span, t_eval)
        
        # Create animation with proper spacing
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor('#1a1a1a')  # Dark background for consistency
        
        def update(frame):
            ax.clear()
            im = ax.contourf(self.X, self.Y, solutions[frame], levels=20, cmap='hot')
            ax.set_title(f'Radial Diffusion Field - t={t_eval[frame]:.2f}', 
                        fontsize=12, color='white', weight='bold', pad=12)
            ax.set_xlabel('x', fontsize=10, color='white')
            ax.set_ylabel('y', fontsize=10, color='white')
            ax.set_facecolor('#0a0e27')  # Dark axes
            ax.tick_params(colors='white', labelsize=8)
            return [im]
        
        anim = animation.FuncAnimation(fig, update, frames=len(solutions), 
                                      interval=100, blit=True, repeat=True)
        # Proper spacing: tight layout with padding
        plt.tight_layout(pad=1.5, w_pad=0.5, h_pad=1.0)
        anim.save(output_file, writer='pillow', dpi=100)
        plt.close()
        
        return output_file
    
    def generate_linear_field_simulation(self, output_file="linear_simulation.gif"):
        """Generate animated linear propagation field"""
        
        # Initial step function on left side
        initial = np.zeros((self.resolution, self.resolution))
        initial[:, :self.resolution//2] = 1.0
        
        # Solve with stronger linear term (simulates sharp front)
        t_span = (0, 0.5)
        t_eval = np.linspace(0, 0.5, 20)
        solutions = self.solve_diffusion_equation(initial, t_span, t_eval)
        
        # Create animation with proper spacing
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#1a1a1a')  # Dark background for consistency
        
        def update(frame):
            ax.clear()
            ax.contourf(self.X, self.Y, solutions[frame], levels=20, cmap='RdYlBu_r')
            ax.set_title(f'Linear Propagation - t={t_eval[frame]:.2f}', 
                        fontsize=12, color='white', weight='bold', pad=12)
            ax.set_xlabel('x', fontsize=10, color='white')
            ax.set_ylabel('y', fontsize=10, color='white')
            ax.set_facecolor('#0a0e27')  # Dark axes
            ax.tick_params(colors='white', labelsize=8)
            return []
        
        anim = animation.FuncAnimation(fig, update, frames=len(solutions),
                                      interval=100, blit=False, repeat=True)
        # Proper spacing: tight layout with padding
        plt.tight_layout(pad=1.5, w_pad=0.5, h_pad=1.0)
        anim.save(output_file, writer='pillow', dpi=100)
        plt.close()
        
        return output_file
    
    def generate_cascade_field_simulation(self, output_file="cascade_simulation.gif"):
        """Generate animated exponential cascade field"""
        
        # Small initial condition
        initial = np.ones((self.resolution, self.resolution)) * 0.01
        initial[self.resolution//2-5:self.resolution//2+5, 
                self.resolution//2-5:self.resolution//2+5] = 0.5
        
        # Solve with strong beta term (enables cascade)
        t_span = (0, 0.2)
        t_eval = np.linspace(0, 0.2, 25)
        
        # Temporarily increase beta for dramatic cascade effect
        old_beta = self.beta
        self.beta = 1.0  # Strong nonlinearity
        solutions = self.solve_diffusion_equation(initial, t_span, t_eval)
        self.beta = old_beta
        
        # Create animation with proper spacing
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor('#1a1a1a')  # Dark background for consistency
        
        def update(frame):
            ax.clear()
            vmax = np.percentile(solutions[frame], 95)
            im = ax.contourf(self.X, self.Y, solutions[frame], levels=20, 
                            cmap='hot', vmax=vmax)
            ax.set_title(f'Cascade/Exponential Growth - t={t_eval[frame]:.3f}', 
                        fontsize=12, color='white', weight='bold', pad=12)
            ax.set_xlabel('x', fontsize=10, color='white')
            ax.set_ylabel('y', fontsize=10, color='white')
            ax.set_facecolor('#0a0e27')  # Dark axes
            ax.tick_params(colors='white', labelsize=8)
            cbar = plt.colorbar(im, ax=ax, label='ρ(x,y,t)')
            cbar.set_label('ρ(x,y,t)', color='white', fontsize=9)
            cbar.ax.tick_params(colors='white', labelsize=8)
            return []
        
        anim = animation.FuncAnimation(fig, update, frames=len(solutions),
                                      interval=100, blit=False, repeat=True)
        # Proper spacing: tight layout with padding
        plt.tight_layout(pad=1.5, w_pad=0.5, h_pad=1.0)
        anim.save(output_file, writer='pillow', dpi=100)
        plt.close()
        
        return output_file
    
    def generate_phase_diagram(self, output_file="phase_diagram.png"):
        """Generate phase diagram showing cascade behavior"""
        
        # Vary alpha and beta, show which regions exhibit strong cascading
        alphas = np.linspace(-0.2, 0.5, 50)
        betas = np.linspace(0, 2.0, 50)
        
        cascade_strength = np.zeros((len(betas), len(alphas)))
        
        for i, beta in enumerate(betas):
            for j, alpha in enumerate(alphas):
                # Test initial condition evolution
                rho0 = 0.1
                # Simple growth model: τ ≈ 1 / (alpha + beta*rho0)
                if alpha + beta * rho0 > 0:
                    cascade_strength[i, j] = np.log(1 + alpha + beta * rho0)
                else:
                    cascade_strength[i, j] = 0
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        im = ax.contourf(alphas, betas, cascade_strength, levels=20, cmap='viridis')
        ax.set_xlabel('Linear Response (α)', fontsize=12)
        ax.set_ylabel('Nonlinear Response (β)', fontsize=12)
        ax.set_title('Cascade Strength Phase Diagram\n(dρ/dt = D·∇²ρ + α·ρ + β·ρ²)', fontsize=14)
        
        cbar = plt.colorbar(im, ax=ax, label='Cascade Strength')
        
        # Mark cascade boundary
        cascade_boundary = -0.5 / betas
        ax.plot(cascade_boundary, betas, 'r--', linewidth=2, label='Stability Boundary')
        ax.legend()
        
        ax.set_xlim([alphas.min(), alphas.max()])
        ax.set_ylim([betas.min(), betas.max()])
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        return output_file
    
    def get_image_as_base64(self, image_file):
        """Convert image to base64 for embedding in HTML/JSON"""
        with open(image_file, 'rb') as f:
            image_data = f.read()
        return base64.b64encode(image_data).decode('utf-8')
    
    def generate_json_api_response(self, field_name, parameters):
        """
        Generate JSON response for web API
        
        Can be used by web frontend to request custom visualizations
        """
        return {
            "field_name": field_name,
            "parameters": {
                "D": self.D,
                "alpha": self.alpha,
                "beta": self.beta,
                "domain_size": self.domain_size,
                "resolution": self.resolution
            },
            "description": f"Universal Diffusion Field: {field_name}",
            "equation": "dρ/dt = D·∇²ρ + α·f_external + β·ρ²",
            "import_instructions": "3-4 lines to use this field",
            "cross_references": ["Related Field 1", "Related Field 2"]
        }

# Example: Flask web server for dynamic field generation
if __name__ == "__main__":
    print("\n" + "="*60)
    print("DYNAMIC FIELD VISUALIZATION GENERATOR")
    print("="*60 + "\n")
    
    # Create generator with standard parameters
    gen = DynamicFieldGenerator(D=0.1, alpha=0.05, beta=0.5)
    
    # Generate example simulations
    print("Generating animated field simulations...")
    print("(This creates GIF files showing cascade dynamics over time)\n")
    
    print("1. Radial diffusion simulation...")
    gen.generate_radial_field_simulation("radial_dynamic_sim.gif")
    print("   ✓ Saved radial_dynamic_sim.gif\n")
    
    print("2. Linear propagation simulation...")
    gen.generate_linear_field_simulation("linear_dynamic_sim.gif")
    print("   ✓ Saved linear_dynamic_sim.gif\n")
    
    print("3. Cascade/exponential growth simulation...")
    gen.generate_cascade_field_simulation("cascade_dynamic_sim.gif")
    print("   ✓ Saved cascade_dynamic_sim.gif\n")
    
    print("4. Phase diagram showing cascade regions...")
    gen.generate_phase_diagram("phase_diagram.png")
    print("   ✓ Saved phase_diagram.png\n")
    
    print("="*60)
    print("✓ DYNAMIC VISUALIZATIONS GENERATED")
    print("="*60 + "\n")
    
    print("Next steps:")
    print("1. Use field_visualization_system.py for static wiki images")
    print("2. Use this script for animated simulations")
    print("3. Deploy as web service for real-time generation:")
    print("   - FastAPI/Flask backend: handle requests")
    print("   - Return base64-encoded images or GIF streams")
    print("   - Client-side: display in browser or Jupyter")
    print("\n")
