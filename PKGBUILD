pkgname=govix-calc
pkgver=1.0
pkgrel=1
pkgdesc="Dual-panel Qt-based calculator built with PySide6"
arch=('any')
url="https://github.com/yourusername/govix-calc"  # or your personal page
license=('MIT')
depends=('python' 'python-pyside6')
makedepends=('python-setuptools')
source=("govix-calc.tar.gz")
sha256sums=('SKIP')  # Use updpkgsums to update it

build() {
    cd "$srcdir/$pkgname"
    # Optional: python setup.py build
}

package() {
    cd "$srcdir/$pkgname"

    install -Dm755 main.py "$pkgdir/usr/bin/govix-calc"
    sed -i '1i#!/usr/bin/env python' "$pkgdir/usr/bin/govix-calc"

    mkdir -p "$pkgdir/usr/lib/govix-calc/"
    cp -r govix_calc/*.py "$pkgdir/usr/lib/govix-calc/"
}
