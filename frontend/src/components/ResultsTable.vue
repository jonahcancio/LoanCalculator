<template>
  <b-modal id="results_modal" size="lg">
    <template v-slot:modal-title>
    <h2 >Loan Inquiry Results</h2>
    </template>
    <b-table bordered striped hover :items="items"></b-table>
  </b-modal>
</template>

<script>
export default {
  props: {
    data: Object,
  },
  data() {
    return {
      money_formatter: new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP', currencyDisplay:'narrowSymbol' })
    }
  },
  computed: {
    items() {
      if (!this.data) {
        return null;
      }
      return [
        { description: "Loan Type", details: this.data["loan_type"] },
        {
          description: "Principal Amount",
          details: this.money_string(this.data["principal_amount"]),
        },
        {
          description: "Monthly Amortization",
          details: this.money_string(this.data["monthly_amortization"]),
        },
        {
          description: "Total Interest",
          details: this.money_string(this.data["total_interest"]),
        },
        {
          description: "Loan Term",
          details: `${this.data["loan_term"]} months`
        },
        {
          description: "Total Sum of Payments upon loan maturity",
          details: this.money_string(this.data["sum_payments"]),
        },
        {
          description: "Loan Start Date",
          details: new Date(this.data["loan_start_date"]).toDateString(),
        },
        {
          description: "First Loan Payment Date",
          details: new Date(this.data["first_payment_date"]).toDateString()
        },
        {
          description: "Loan Maturity Date",
          details: new Date(this.data["loan_maturity_date"]).toDateString()
        },
      ];
    },
  },
  methods: {
    money_string(value) {
      // return `₱ ${value.toFixed(2)}`
      return this.money_formatter.format(value);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
