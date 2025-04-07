import io
import pandas as pd


def write_cc_fit_data(filename, param_dict, gen_data, apply_data):
    # param_dict = {key: np.array([value]) for (key, value) in param_dict.items()}
    param_dict = {key: [str(value)] for (key, value) in param_dict.items()}
    out_dict = {}
    if gen_data.breakpoint_lim:
        out_dict["Estimated t_cont"] = gen_data.est_t_cont
    if gen_data.fit_eq is not None:
        out_dict["Coefficients"] = gen_data.params
        if gen_data.lol:
            out_dict["Limit of Linearity"] = gen_data.lol
        if gen_data.mec:
            out_dict["Molar Extinction Coefficent"] = gen_data.mec
        if gen_data.mol0_fit is not None:
            out_dict["mol0_fit"] = gen_data.mol0_fit
        out_dict.update({"RSS": gen_data.rss,
                         "RMSE": gen_data.rmse,
                         "MAE": gen_data.mae,
                         "R2": gen_data.r2,
                         "R2_adj": gen_data.r2_adj,
                         "AIC": gen_data.aic,
                         "BIC": gen_data.bic})

    writer = pd.ExcelWriter(filename, engine='openpyxl')
    if apply_data is not None:
        apply_data.all_df.to_excel(writer, sheet_name='ApplicationData')
    gen_data.all_df.to_excel(writer, sheet_name='GenerationData')
    if out_dict:
        pd.DataFrame.from_dict(out_dict).to_excel(writer, sheet_name='OutputParams')
    pd.DataFrame.from_dict(param_dict).to_excel(writer, sheet_name='InputParams')
    writer.save()


def write_cc_fit_data_temp(param_dict, gen_data, apply_data):
    tmp_file = io.BytesIO()
    write_cc_fit_data(tmp_file, param_dict, gen_data, apply_data)

    return tmp_file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


# print CC results
def pprint_cc(data):
    if data.num_spec == 1 and data.params is not None:
        result = f"""
Parameters:     { {item: f"{value:.4g}" for item, value in data.params[0].items()} }
Est. Error +/-: { {item: f"{value:.2g}" for item, value in data.param_err[0].items()} }\n
"""

        if data.breakpoint_lim:
            result += f"Estimated t_cont: {[f'{item:.4g}' for item in data.est_t_cont[0]]}\n"
        if data.lol is not None:
            result += f"Limits of Linearity: {data.lol[0]:.4g}\n"
        if data.mec is not None:
            result += f"Molar Extinction Coefficient: {data.mec[0]:.4g}\n"
        if data.mol0_fit is not None:
            result += f"Fitted initial moles: {data.mol0_fit[0]:.4g}\n"

        result += f"""
Quality of Fit Metrics:
RMSE: {data.rmse[0]:.4g} | MAE: {data.mae[0]:.4g}
        """
        if data.r2:
            result += f"""
R²: {data.r2[0]:.4g} | Adjusted R²: {data.r2_adj[0]:.4g}
AIC: {data.aic[0]:.4g} | BIC: {data.bic[0]:.4g}
"""

    else:
        result = f"Download file to see results"

    return result