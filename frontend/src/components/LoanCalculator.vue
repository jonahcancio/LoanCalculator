<template>
  <b-container>
    <h1>LOAN CALCULATOR</h1>
    <b-row>
      <b-col>
        <b-card border-variant="primary" header="Loan Inputs">
          <b-form-group
            label="Loan Type"
            label-size="sm"
            label-align="left"
            :state="validation.loan_type"
            :invalid-feedback="invalid_feedback.loan_type"
          >
            <b-form-select
              v-model="payload.loan_type"
              :options="loan_type_options"
              size="sm"
              :state="validation.loan_type"
              :invalid-feedback="invalid_feedback.loan_type"
            />
          </b-form-group>
          <b-form-group
            v-if="payload.loan_type == 'A'"
            label="Principal Amount (₱)"
            label-size="sm"
            label-align="left"
            :state="validation.principal_amount"
            :invalid-feedback="invalid_feedback.principal_amount"
          >
            <b-form-input
              id="principal_amount"
              type="number"
              size="sm"
              v-model="payload.principal_amount"
              number
              min="10000"
              :state="validation.principal_amount"
            />
          </b-form-group>
          <b-form-group
            v-else-if="payload.loan_type == 'B'"
            label="Monthly Amortization (₱)"
            label-size="sm"
            label-align="left"
            :state="validation.monthly_amortization"
            :invalid-feedback="invalid_feedback.monthly_amortization"
          >
            <b-form-input
              id="monthly_amortization"
              type="number"
              size="sm"
              v-model="payload.monthly_amortization"
              number
              min="1000"
              :state="validation.monthly_amortization"
            />
          </b-form-group>
          <b-form-group
            label="Loan Term (months)"
            label-size="sm"
            label-align="left"
            :state="validation.loan_term"
            :invalid-feedback="invalid_feedback.loan_term"
          >
            <b-form-input
              id="loan_term"
              type="number"
              size="sm"
              number
              v-model="payload.loan_term"
              v-bind="loan_term_props"
              :state="validation.loan_term"
            />
          </b-form-group>
          <b-form-group
            label="Loan Start Date"
            label-size="sm"
            label-align="left"
          >
            <b-form-input
              id="loan_start_date"
              type="date"
              size="sm"
              v-model="payload.loan_start_date"
              :state="validation.loan_start_date"
            />
          </b-form-group>
        </b-card>
        <b-button
          @click="calculate"
          variant="primary"
          block
          class="mt-3"
          :disabled="!is_all_validated"
          >Calculate</b-button
        >
      </b-col>
      <b-col>
        <b-card border-variant="secondary" header="Other Inputs">
          <b-form-group label="Full Name" label-size="sm" label-align="left">
            <b-form-input
              id="full_name"
              type="text"
              size="sm"
              v-model="payload.full_name"
            />
          </b-form-group>
          <b-form-group label="Email" label-size="sm" label-align="left">
            <b-form-input
              id="email"
              type="email"
              size="sm"
              v-model="payload.email"
            />
          </b-form-group>
          <b-form-group
            label="Mobile Number"
            label-size="sm"
            label-align="left"
          >
            <b-form-input
              id="mobile_number"
              type="text"
              size="sm"
              v-model="payload.mobile_number"
            />
          </b-form-group>
          <b-form-group label="City" label-size="sm" label-align="left">
            <b-form-input
              id="city"
              type="text"
              size="sm"
              v-model="payload.city"
            />
          </b-form-group>
          <b-form-group label="Province" label-size="sm" label-align="left">
            <b-form-input
              id="province"
              type="text"
              size="sm"
              v-model="payload.province"
            />
          </b-form-group>
        </b-card>
      </b-col>
    </b-row>

    <div>
      <ResultsTable :data="results_data" />
      <b-modal id="error_modal" size="lg">
        <template v-slot:modal-title>
          <h2>An Error Occurred</h2>
        </template>
        {{ error_data }}
      </b-modal>
    </div>
  </b-container>
</template>

<script>
import ResultsTable from "./ResultsTable";
export default {
  components: {
    ResultsTable,
  },
  data() {
    return {
      payload: {
        loan_type: null,
        principal_amount: 10000,
        monthly_amortization: 1000,
        loan_term: 6,
        loan_start_date: new Date(Date.now()).toISOString().slice(0, 10),
        full_name: "",
        email: "",
        mobile_number: "",
        city: "",
        province: "",
      },
      results_data: null,
      error_data: null,
    };
  },
  computed: {
    loan_type_options() {
      return [
        { value: null, text: "Select loan type", disabled: true },
        "A",
        "B",
      ];
    },
    loan_term_props() {
      if (this.payload.loan_type == "A") {
        return {
          min: 3,
          max: 18,
          step: 3,
        };
      } else if (this.payload.loan_type == "B") {
        return {
          min: 6,
          max: 18,
          step: 1,
        };
      }
      return {
        min: 0,
        max: 0,
        step: 0,
      };
    },
    validation() {
      const { payload } = this;
      return {
        loan_type: payload.loan_type == "A" || payload.loan_type == "B",
        principal_amount: payload.principal_amount >= 10000,
        monthly_amortization: payload.monthly_amortization >= 1000,
        loan_term:
          (payload.loan_type == "A" &&
            payload.loan_term >= 3 &&
            payload.loan_term <= 18 &&
            payload.loan_term % 3 == 0) ||
          (payload.loan_type == "B" &&
            payload.loan_term >= 6 &&
            payload.loan_term <= 18 &&
            payload.loan_term % 1 == 0),
        loan_start_date: Date.parse(payload.loan_start_date) ? true : false,
      };
    },
    invalid_feedback() {
      const { payload } = this;
      return {
        loan_type: "must be either A or B",
        principal_amount: "must be greater than P10000",
        monthly_amortization: "must be greater than P1000",
        loan_term:
          (payload.loan_type == "A" &&
            "Must be between 3-18 months and a multiple of 3") ||
          (payload.loan_type == "B" && "Must be between 6-18 months") ||
          "",
        loan_start_date: "must be a valid date",
      };
    },
    is_all_validated() {
      for (let flag of Object.values(this.validation)) {
        if (!flag) return false;
      }
      return true;
    },
  },
  methods: {
    calculate() {
      this.$axios
        .post("http://localhost:8000/calculator/", this.payload)
        .then((response) => {
          console.log("RESULTS: ", response.data);
          this.results_data = response.data;
          this.$bvModal.show("results_modal");
        })
        .catch((error) => {
          this.error_data = error.response ? error.response.data : error;
          console.log(this.error_data)
          this.$bvModal.show("error_modal");
        });
    },
  },
};
</script>

<style>
.invalid-feedback {
  text-align: left;
}
</style>
