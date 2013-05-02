#!/bin/bash
# atualiza tag "release" para apontar para a revisao corrente

# deleta a tag release aqui e remotamente
git tag -d release
git push origin :release

# recria a tag release e envia tudo
git tag release
git push
git push --all
git push --tags
