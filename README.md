# TMS para Odoo 18.0

Backport a Odoo 18.0 de los submódulos de transporte de
[OCA/stock-logistics-transport](https://github.com/OCA/stock-logistics-transport)
(rama 17.0, commit `8476a3e`), que no existen en la rama 18.0 de OCA.

| Módulo | Descripción |
| --- | --- |
| `tms_product` | Productos transportables y vehículos desde productos |
| `tms_purchase` | Compras vinculadas a viajes |
| `tms_sale` | Venta de viajes y boletos |
| `tms_expense` | Gastos de viaje |
| `tms_account` | Facturación de viajes y contabilidad analítica por ruta/viaje |
| `tms_account_asset` | Vehículos como activos contables |

Requiere el módulo `tms` de OCA/stock-logistics-transport 18.0.

## Adaptaciones respecto de 17.0

- `tree` → `list`, `detailed_type` → `type`, `create` en batch.
- Impuestos con `tms_factor` sobre `_prepare_base_line_for_taxes_computation`
  (venta) y `_prepare_product_base_line_for_taxes_computation` (factura).
- Columnas analíticas por `plan._column_name()` en lugar de `x_planN_id`.
- Correcciones: grupos de planes analíticos, recálculo de `tms_factor` al elegir
  la ruta, empleados solo para conductores internos, rendición de gastos al
  completar el viaje.

Licencia AGPL-3.
