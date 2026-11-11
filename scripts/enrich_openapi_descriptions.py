#!/usr/bin/env python3
"""Fill in missing/thin operation descriptions in openapi/d4sign.yaml.

Source: the real docapi.d4sign.com.br guide pages (a scraped copy of them,
external to this repo). Many operations in the spec were exported with an
empty or one-line description even though the real docs have full prose +
parameter tables for them. UPDATES below only covers those — operations
that already carry the full exported prose (e.g. createlist,
addsignaturetype) are left untouched.

Run once; re-run is safe (idempotent — same content in, same content out).
"""
from __future__ import annotations

import io
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString as LS

SPEC_PATH = Path(__file__).resolve().parent.parent / "openapi" / "d4sign.yaml"

INFO_DESCRIPTION = LS(
    "A D4Sign é uma plataforma de assinatura eletrônica de documentos que atende os "
    "requisitos da Medida Provisória 2.200-2/01 (autenticidade, integridade e não "
    "repúdio), trazendo validade jurídica para as assinaturas realizadas através da "
    "D4Sign.\n"
    "\n"
    "API RESTful, respostas em JSON. Toda requisição deve enviar `tokenAPI` e "
    "`cryptKey` (`?tokenAPI={token}&cryptKey={cryptKey}`) — veja o esquema de "
    "segurança abaixo. Limite padrão: **10 requisições por hora** por conta; para "
    "aumentar, contato comercial@d4sign.com.br.\n"
    "\n"
    "Collection Postman oficial: https://documenter.getpostman.com/view/1486030/d4sign-api/2TnpL3 "
    "(host padrão configurado é o de Sandbox).\n"
)

# (method, path) -> markdown description. Paths match openapi/d4sign.yaml exactly.
UPDATES: dict[tuple[str, str], str] = {
    ("get", "/api/v1/safes"): (
        "Lista TODOS os cofres da conta.\n"
        "\n"
        "> Não esqueça de enviar `tokenAPI` e `cryptKey` na requisição.\n"
    ),
    ("post", "/api/v1/folders/{uuid_safe}/create"): (
        "Cria uma pasta (ou subpasta) dentro do cofre informado.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `uuid_folder` (opcional) | UUID da pasta pai, para criar uma subpasta. |\n"
        "| `folder_name` (obrigatório) | Nome da pasta ou subpasta. |\n"
    ),
    ("post", "/api/v1/folders/{uuid_safe}/rename"): (
        "Renomeia uma pasta ou subpasta dentro do cofre informado.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `folder_name` (obrigatório) | Novo nome da pasta ou subpasta. |\n"
        "| `uuid_folder` (obrigatório) | UUID da pasta ou subpasta a renomear. |\n"
    ),
    ("get", "/api/v1/folders/{uuid_safe}/find"): (
        "Lista TODAS as pastas do cofre informado.\n"
    ),
    ("post", "/api/v1/batches"): (
        "Cria um lote de documentos a partir de uma lista de UUIDs.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `keys` (obrigatório) | UUIDs dos documentos que farão parte do lote. **Máximo de 25 documentos por lote.** |\n"
    ),
    ("get", "/api/v1/account/balance"): "Retorna o balanço (créditos) da conta.\n",
    ("get", "/api/v1/testcall"): (
        "Endpoint simples para testar conectividade e credenciais (`tokenAPI`/`cryptKey`) sem efeitos colaterais.\n"
    ),
    ("get", "/api/v1/documents"): (
        "Lista TODOS os documentos da conta.\n"
        "\n"
        "> Paginado em blocos de 500 documentos. Use o parâmetro `pg` na URL para paginar "
        "(ex.: `?pg=2`). O primeiro bloco do resultado traz o total de páginas disponíveis.\n"
    ),
    ("get", "/api/v1/documents/{uuid_document}"): "Retorna apenas o documento solicitado.\n",
    ("get", "/api/v1/documents/{uuid_document}/dimensions"): (
        "Retorna as dimensões (largura/altura em px), por página, de um documento.\n"
    ),
    ("get", "/api/v1/documents/{id_status}/status"): (
        "Lista todos os documentos que estiverem na fase informada.\n"
        "\n"
        "| ID | Fase |\n"
        "| --- | --- |\n"
        "| 1 | Processando |\n"
        "| 2 | Aguardando Signatários |\n"
        "| 3 | Aguardando Assinaturas |\n"
        "| 4 | Finalizado |\n"
        "| 5 | Arquivado |\n"
        "| 6 | Cancelado |\n"
        "| 7 | Editando |\n"
        "\n"
        "> Paginado em blocos de 500 documentos — use `pg` na URL.\n"
    ),
    ("get", "/api/v1/documents/{uuid_safe}/safe"): (
        "Lista todos os documentos associados ao cofre (e pasta, se filtrado) informado. "
        "Para filtrar por pasta use `/documents/{uuid_safe}/safe/{uuid_folder}`.\n"
        "\n"
        "> Paginado em blocos de 500 documentos — use `pg` na URL.\n"
    ),
    ("get", "/api/v1/documents/{uuid_safe}/safe/{uuid_folder}"): (
        "Lista todos os documentos associados ao cofre e à pasta informados.\n"
        "\n"
        "> Paginado em blocos de 500 documentos — use `pg` na URL.\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/cancel"): (
        "Cancela o documento. O parâmetro `comment` (opcional) registra o motivo do cancelamento.\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/download"): (
        "Gera uma URL final para download do documento.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `type` (opcional) | `zip` para o arquivo completo, `pdf` para apenas o PDF, `pdfa` para PDF/A. |\n"
        "| `language` (opcional) | `pt` ou `en`. |\n"
        "| `document` (opcional) | `true` inclui no retorno, em base64, as fotos do documento de identidade/selfie usadas na autenticação (quando aplicável). |\n"
        "| `encoding` (opcional) | `1` retorna a URL do arquivo em base64. |\n"
        "\n"
        "> A URL retornada pode conter `&` — trate-a (coloque entre aspas) antes de usar em shells como o PowerShell.\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/resend"): (
        "Reenvia o link de assinatura para o signatário (`email` ou WhatsApp + `key_signer`).\n"
        "\n"
        "> Intervalos entre reenvios: 1º em 1 min, 2º em 5 min, 3º em 30 min; a partir do 4º, de 60 em 60 min.\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/scheduling"): (
        "Agenda o envio do documento para assinatura em uma data/hora futura.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `message` (opcional) | Mensagem enviada aos signatários no envio. |\n"
        "| `workflow` (obrigatório) | `1` = não seguir a ordem de assinatura; `2` = seguir a ordem. |\n"
        "| `scheduling_date` (obrigatório) | Data (>= hoje), formato `aaaa/mm/dd`. |\n"
        "| `scheduling_time` (obrigatório) | Hora cheia entre 06:00 e 22:00 (ex.: `11:00`); se a data for hoje, deve ser maior que a hora atual. |\n"
        "| `urgent_document` (opcional) | `1` = documento urgente. |\n"
    ),
    ("get", "/api/v1/documents/{uuid_document}/powerformresponses"): (
        "Lista as respostas preenchidas em um Power Form (documento gerado a partir de um link público preenchível).\n"
    ),
    ("post", "/api/v1/certificate/uuid-documento/list"): (
        "Lista o certificado definido para o signatário (`key_signer`).\n"
    ),
    ("post", "/api/v1/certificate/uuid-documento/add"): (
        "Define o tipo de certificado digital exigido do signatário.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `key_signer` (obrigatório) | Chave do signatário. |\n"
        "| `document_type` (obrigatório) | `1` = qualquer certificado, `2` = e-CPF, `3` = e-CNPJ. |\n"
        "| `pades` (opcional) | `1` = PAdES e CAdES, `0` = apenas CAdES. |\n"
        "| `document_number` (opcional) | CPF/CNPJ do signatário; em branco aceita qualquer e-CPF/e-CNPJ. |\n"
    ),
    ("get", "/api/v1/watcher/{uuid_document}"): "Lista todos os observadores (watchers) do documento.\n",
    ("post", "/api/v1/watcher/{uuid_document}/add"): (
        "Adiciona um observador ao documento.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `email` (obrigatório) | E-mail do observador. |\n"
        "| `permission` (opcional) | `0` = perfil básico (pode baixar), `1` = apenas visualização (sem download). |\n"
    ),
    ("post", "/api/v1/watcher/{uuid_document}/remove"): "Remove um observador (`email`) do documento.\n",
    ("post", "/api/v1/watcher/{uuid_document}/erase"): "Remove TODOS os observadores do documento.\n",
    ("get", "/api/v1/groups/{uuid_safe}"): "Lista todos os grupos de assinatura do cofre.\n",
    ("get", "/api/v1/groups/{uuid_safe}/groupdetails/{uuid_group}"): (
        "Lista os detalhes de um grupo de assinatura — apenas se o `tokenAPI` é o dono da conta do "
        "`uuid_grupo`, ou se o grupo está compartilhado no `uuid_safe` informado.\n"
    ),
    ("get", "/api/v1/documents/{uuid_document}/list"): "Lista todos os signatários de um documento, com status e dados de assinatura (IP, geolocalização, data).\n",
    ("post", "/api/v1/documents/{uuid_document}/changeemail"): (
        "Atualiza o e-mail (ou WhatsApp) de um signatário já cadastrado.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `email-before` (obrigatório) | E-mail/WhatsApp atual do signatário. |\n"
        "| `email-after` (obrigatório) | Novo e-mail/WhatsApp. |\n"
        "| `key-signer` | Chave do signatário (obtida ao listar signatários do documento). |\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/changesmsnumber"): (
        "Atualiza o número de SMS/WhatsApp de um signatário.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `email` (obrigatório) | E-mail do signatário. |\n"
        "| `sms-number` (obrigatório) | Novo número, formato `+5511953874555`. |\n"
        "| `key-signer` | Chave do signatário. |\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/changepasswordcode"): (
        "Atualiza o código de acesso do signatário (deixe `password-code` em branco para remover o código atual).\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/removeemaillist"): (
        "Remove um signatário (`email-signer` + `key-signer`) do documento.\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/addpins"): (
        "Adiciona uma assinatura/rubrica/selo posicionado (pin) no documento principal ou anexo.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `document` (obrigatório) | UUID do documento principal ou anexo (slave). |\n"
        "| `email` (obrigatório) | E-mail do signatário já cadastrado no documento. |\n"
        "| `page_width`/`page_height` (obrigatório) | Dimensões da página, em px. |\n"
        "| `page` (obrigatório) | Página onde o pin ficará. |\n"
        "| `position_x`/`position_y` (obrigatório) | Posição do pin, em px. |\n"
        "| `type` (opcional) | `0` = assinatura, `1` = rubrica, `2` = selo. |\n"
        "\n"
        "> Para o UUID de um anexo (slave), use `GET /documents/{uuid_document}/listslaves`.\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/removepins"): (
        "Remove uma assinatura/rubrica posicionada (pin) do documento, por `email`, `page`, `position_x`, `position_y`.\n"
    ),
    ("get", "/api/v1/documents/{uuid_document}/listpins"): (
        "Lista as assinaturas/rubricas posicionadas (pins) em um documento, com página e coordenadas.\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/addpinswithreplics"): (
        "Replica uma posição de assinatura em TODAS as páginas do documento principal e, opcionalmente, de anexos "
        "(`document_slaves`).\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `email` (obrigatório) | Signatário já cadastrado no documento. |\n"
        "| `page_width`/`page_height` (obrigatório) | Dimensões da página, em px. |\n"
        "| `position_x`/`position_y` (obrigatório) | Posição, em mm. |\n"
        "| `type` (opcional) | `0` = assinatura, `1` = rubrica, `2` = selo. |\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/removepinswithreplics"): (
        "Remove as posições de assinatura replicadas (ver `addpinswithreplics`) no documento principal e anexos, "
        "por `email`, `position_x`, `position_y`.\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/addinfo"): (
        "Cadastra nome, CPF e data de nascimento de um signatário — **apenas para assinatura presencial**. "
        "Útil para evitar que o signatário precise informar esses dados no momento da assinatura.\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/addtrustid"): (
        "Ativa o Trust ID (verificação extra de identidade via documento com foto, opcionalmente + selfie) "
        "para um ou mais signatários já cadastrados com `docauth` ou `docauthandselfie` habilitado.\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `email` (obrigatório) | Signatário já cadastrado com ponto de autenticação por documento (+selfie). |\n"
        "| `document_type` (obrigatório) | `1` = documento de identidade nacional, `2` = passaporte, `3` = permissão de residência, `4` = outro. |\n"
        "| `name`/`last_name`/`document_number` (opcionais) | Dados do signatário. |\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/removetrustid"): (
        "Remove a verificação Trust ID previamente adicionada a um ou mais signatários (`email`).\n"
    ),
    ("get", "/api/v1/documents/{uuid_document}/signaturelink/{id_link_assinatura}"): (
        "Retorna o link de assinatura de um signatário específico. Só disponível depois que o documento foi "
        "enviado para o signatário; requer ser dono do cofre ou ter permissão administrador/padrão em cofre "
        "compartilhado.\n"
    ),
    ("post", "/api/v1/documents/{uuid_safe}/createrubricintemplateword"): (
        "Gera um documento a partir de um template Word com rubricas posicionadas por token, no cofre informado.\n"
        "\n"
        "Fluxo: liste os templates (`POST /templates`) para obter o `id`, liste os cofres (`GET /safes`) para "
        "obter o `uuid_safe`, e então use este endpoint informando `templates.{id}.{token}` = e-mail do "
        "signatário correspondente a cada rubrica.\n"
    ),
    ("get", "/api/v1/documents/{uuid_document}/listslaves"): (
        "Lista os anexos (documentos secundários) vinculados a um documento principal.\n"
    ),
    ("post", "/api/v1/documents/{uuid_document}/downloadlist"): (
        "Gera uma URL para download em lote de documentos (principal e/ou anexos) e, opcionalmente, suas hashes "
        "(certificados de assinatura).\n"
        "\n"
        "| Parâmetro | Descrição |\n"
        "| --- | --- |\n"
        "| `language` (opcional) | `pt` ou `en`. |\n"
        "| `type` (opcional) | Omitir para PDF; `pdfa` para PDF/A. |\n"
        "| `documents` (obrigatório) | Mapa `{uuid-documento: \"1\"|\"0\"}` — `1` inclui a hash/certificado junto ao documento. |\n"
        "\n"
        "> O documento precisa estar finalizado (todos os signatários assinaram).\n"
    ),
    ("post", "/api/v1/documents/{uuid_safe}/uploadbigfile"): (
        "Upload de documento principal ACIMA de 20MB e menor que 500MB (mesmo contrato do `/upload` padrão).\n"
    ),
    ("get", "/api/v1/users/list"): (
        "Lista todos os usuários do domínio validado da conta.\n"
        "\n"
        "> Paginado em blocos de 500 — use `pg` na URL.\n"
    ),
    ("post", "/api/v1/users/check"): "Verifica o status (`email_user`) de um usuário do domínio validado.\n",
    ("post", "/api/v1/users/block"): "Bloqueia um usuário (`email_user`) do domínio validado.\n",
    ("post", "/api/v1/users/unblock"): "Desbloqueia um usuário (`email_user`) do domínio validado.\n",
    ("get", "/api/v1/documents/{uuid_document}/webhooks"): "Lista o(s) webhook(s) (POSTBack) cadastrado(s) no documento.\n",
    ("post", "/api/v1/documents/{uuid_document}/webhooks"): (
        "Cadastra uma URL de webhook (POSTBack) no documento. D4Sign dispara um `POST` em form-data para essa "
        "URL quando o documento é assinado, finalizado, cancelado, ou quando um e-mail não é entregue a um "
        "signatário.\n"
        "\n"
        "> Até 7 tentativas de reenvio caso a URL esteja indisponível (0 min, 1h, 1h, 1h, 6h, 6h, 12h) — o "
        "webhook só se perde se a URL ficar indisponível por mais de 27h. Veja segurança (HMAC) no guia.\n"
    ),
    ("get", "/api/v1/tags/{uuid_document}"): "Lista todas as TAGs do documento.\n",
    ("post", "/api/v1/tags/{uuid_document}/remove"): "Remove uma TAG (`tag`) do documento.\n",
    ("post", "/api/v1/tags/{uuid_document}/erase"): "Remove TODAS as TAGs do documento.\n",
}


def main() -> int:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096  # don't rewrap long lines
    spec = yaml.load(io.StringIO(SPEC_PATH.read_text(encoding="utf-8")))

    spec["info"]["description"] = INFO_DESCRIPTION

    updated = 0
    missing = []
    for (method, path), desc in UPDATES.items():
        item = spec["paths"].get(path)
        if item is None or method not in item:
            missing.append((method, path))
            continue
        item[method]["description"] = LS(desc)
        updated += 1

    with open(SPEC_PATH, "w", encoding="utf-8", newline="\n") as f:
        yaml.dump(spec, f)
    print(f"Updated {updated} operation description(s) + info.description.")
    if missing:
        print("Not found in spec (check path spelling):")
        for m, p in missing:
            print(" ", m.upper(), p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
