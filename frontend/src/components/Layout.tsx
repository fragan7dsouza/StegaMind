import { NavLink } from "@/components/NavLink";
import { Shield } from "lucide-react";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center gap-3">
          <Shield className="h-8 w-8 text-primary" />
          <h1 className="text-2xl font-bold text-foreground">StegaMind</h1>
        </div>
      </header>

      {/* Navigation */}
      <nav className="border-b border-border bg-card">
        <div className="container mx-auto px-4">
          <div className="flex gap-1">
            <NavLink
              to="/hide"
              className="px-6 py-3 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
              activeClassName="text-primary border-b-2 border-primary"
            >
              Hide
            </NavLink>
            <NavLink
              to="/detect"
              className="px-6 py-3 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
              activeClassName="text-primary border-b-2 border-primary"
            >
              Detect
            </NavLink>
            <NavLink
              to="/extract"
              className="px-6 py-3 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
              activeClassName="text-primary border-b-2 border-primary"
            >
              Extract
            </NavLink>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 container mx-auto px-4 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card py-6">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          Built by Fragan Dsouza
        </div>
      </footer>
    </div>
  );
};

export default Layout;
