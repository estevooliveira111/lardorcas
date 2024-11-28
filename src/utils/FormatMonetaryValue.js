let formatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL'
});


export const FormatMonetaryValue = (value) => {
  return formatter.format(value);
}


export const currencyBR = (value) => {
  return formatter.format(value);
}