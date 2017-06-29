# windows-setup.ps1
# Jasmine N. Oliveira
#  Installs the SPECdata enviornment
#  and opens the Setup Wizard for configuration

echo "Installing Conda Environment..."
Try {
    conda env create -n specdata-env -f bin/conda_environment_windows.yml
} Catch {
    echo "Environment already exists.. would you like to reinstall?"
}

echo "Open Environment.."
activate specdata-env

echo "Running Setup Wizard..."
cd ..


python run_wizard.py

