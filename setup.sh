#!/bin/bash
# Quick setup script for Umbrella Gateway + Vanna

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     Umbrella Gateway + Vanna Setup Helper                 ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Step 1: Check if in correct directory
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Checking directory"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "config.py" ] && [ -f "quick_start_flask.py" ]; then
    print_success "In correct directory: $(pwd)"
else
    print_error "Not in Vanna directory!"
    echo "Please run from: /Users/trongpv6/Documents/GitHub/vanna"
    exit 1
fi

# Step 2: Check Python
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Checking Python"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 not found!"
    exit 1
fi

# Step 3: Check dependencies
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Checking dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_package() {
    if python3 -c "import $1" 2>/dev/null; then
        print_success "$1 installed"
        return 0
    else
        print_warning "$1 not installed"
        return 1
    fi
}

MISSING_PACKAGES=0

check_package "requests" || MISSING_PACKAGES=1
check_package "psycopg2" || MISSING_PACKAGES=1
check_package "oracledb" || MISSING_PACKAGES=1
check_package "vanna" || MISSING_PACKAGES=1

if [ $MISSING_PACKAGES -eq 1 ]; then
    echo ""
    print_warning "Some packages missing. Install with:"
    echo "  pip install -e '.[pgvector,oracle]'"
    echo ""
    read -p "Install now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install -e '.[pgvector,oracle]'
        print_success "Dependencies installed"
    else
        print_error "Please install dependencies first"
        exit 1
    fi
fi

# Step 4: Check for auth token
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Checking Umbrella Gateway auth token"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f ".vscode/settings.json" ]; then
    TOKEN=$(grep -o '"umbrella-gateway.authToken"[^,]*' .vscode/settings.json | grep -o 'ug_[^"]*' || echo "")
    
    if [ -n "$TOKEN" ]; then
        print_success "Auth token found in .vscode/settings.json"
        echo "   Token: ${TOKEN:0:20}..."
        
        # Check if token is in config.py
        if grep -q "$TOKEN" config.py; then
            print_success "Token already in config.py"
        else
            print_warning "Token not in config.py"
            echo ""
            echo "To update config.py, run:"
            echo "  sed -i '' \"s/'your-auth-token-here'/'$TOKEN'/g\" config.py"
            echo ""
            read -p "Update config.py now? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                sed -i '' "s/'your-auth-token-here'/'$TOKEN'/g" config.py
                print_success "config.py updated with auth token"
            fi
        fi
    else
        print_error "No auth token found in .vscode/settings.json"
        echo ""
        echo "To get your token:"
        echo "  1. Open VS Code"
        echo "  2. Press Cmd+Shift+P"
        echo "  3. Run: 'Umbrella Gateway: Regenerate Auth Token'"
        echo "  4. Check .vscode/settings.json"
        exit 1
    fi
else
    print_error ".vscode/settings.json not found"
    echo ""
    echo "Please install and configure Umbrella Gateway extension first"
    exit 1
fi

# Step 5: Check Umbrella Gateway server
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Checking Umbrella Gateway server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if curl -s http://localhost:8765/health > /dev/null 2>&1; then
    print_success "Umbrella Gateway server is running"
else
    print_error "Umbrella Gateway server not running"
    echo ""
    echo "To start the server:"
    echo "  1. Open VS Code"
    echo "  2. Press Cmd+Shift+P"
    echo "  3. Run: 'Umbrella Gateway: Start Server'"
    echo "  4. Wait for 'Server started on port 8765' notification"
    echo ""
    print_info "Run this script again after starting the server"
    exit 1
fi

# Step 6: Check databases
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 6: Checking database connections"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check PostgreSQL
if python3 -c "import psycopg2; import config; conn = psycopg2.connect(**config.PGVECTOR_CONFIG); conn.close()" 2>/dev/null; then
    print_success "PgVector database connected (mydb)"
else
    print_warning "PgVector database connection failed"
    echo "   Check credentials in config.py"
fi

# Check Oracle
if python3 -c "import oracledb; import config; db=config.DATA_DB_CONFIG; dsn=oracledb.makedsn(db['host'],db['port'],service_name=db['database']); conn=oracledb.connect(user=db['user'],password=db['password'],dsn=dsn); conn.close()" 2>/dev/null; then
    print_success "Oracle database connected (XEPDB1/hr)"
else
    print_warning "Oracle database connection failed"
    echo "   Check credentials in config.py"
fi

# Step 7: Run comprehensive tests
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 7: Running comprehensive tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
read -p "Run full connection tests? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 test_umbrella_connection.py
    TEST_RESULT=$?
    
    if [ $TEST_RESULT -eq 0 ]; then
        echo ""
        print_success "All tests passed!"
    else
        echo ""
        print_error "Some tests failed"
        exit 1
    fi
fi

# Final summary
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║                  ✅ SETUP COMPLETE!                        ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Everything is ready! Next steps:"
echo ""
echo "1. Start Vanna:"
echo "   $ python3 quick_start_flask.py"
echo ""
echo "2. Open Flask UI:"
echo "   http://localhost:8084"
echo ""
echo "3. Try example queries:"
echo "   • Show me all employees"
echo "   • Top 5 highest paid employees"
echo "   • Employees hired in 2024"
echo ""
echo "📚 Documentation:"
echo "   • README_UMBRELLA_GATEWAY.md  - Complete guide"
echo "   • UMBRELLA_GATEWAY_SETUP.md   - Detailed setup"
echo "   • INTEGRATION_COMPLETE.md     - Quick reference"
echo ""
echo "🎉 Happy querying!"
echo ""
