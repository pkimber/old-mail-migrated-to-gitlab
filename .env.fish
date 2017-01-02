# Set environment variables for this VE
source venv-mail/bin/activate.fish
set -x DEFAULT_FROM_EMAIL "web@pkimber.net"
set -x DJANGO_SETTINGS_MODULE "example_mail.dev_patrick"
set -x MAIL_TEMPLATE_TYPE "django"
set -x MAILGUN_SERVER_NAME "pkimber.net"
set -x MANDRILL_API_KEY "abc"
set -x MANDRILL_USER_NAME "def"
set -x RECAPTCHA_PRIVATE_KEY "your private key"
set -x RECAPTCHA_PUBLIC_KEY "your public key"
set -x SECRET_KEY "the_secret_key"
set -x SPARKPOST_API_KEY "ghi"
set -x STRIPE_PUBLISH_KEY "your_stripe_publish_key"
set -x STRIPE_SECRET_KEY "your_stripe_secret_key"
set -x TEST_EMAIL_ADDRESS_1 "test@pkimber.net"
set -x TEST_EMAIL_ADDRESS_2 "test@pkimber.net"
source .private
