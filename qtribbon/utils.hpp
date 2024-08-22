//
// Created by hailin on 8/21/2024.
//

#ifndef PYQTRIBBON_UTILS_HPP
#define PYQTRIBBON_UTILS_HPP

#include <QDir>
#include <QString>

namespace qtribbon {

inline QString DataFile(const QString& filename) {
    QDir dir = QDir::currentPath();
    return dir.absoluteFilePath(filename);
}
}  // namespace qtribbon

#endif  // PYQTRIBBON_UTILS_HPP
